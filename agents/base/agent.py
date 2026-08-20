"""
Ventura Labs AI - Base Agent
Classe base para os agentes do ecossistema.
"""

from __future__ import annotations

import asyncio
import logging
import time
import uuid
from abc import ABC, abstractmethod
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from core.config import AutonomyLevel, Jurisdiction, get_settings

logger = logging.getLogger(__name__)


class AgentStatus(StrEnum):
    IDLE = "idle"
    PROCESSING = "processing"
    WAITING_APPROVAL = "waiting_approval"
    ERROR = "error"
    DISABLED = "disabled"


class TaskPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AgentTask(BaseModel):
    """Representa uma tarefa atribuída a um agente"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""
    task_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    priority: TaskPriority = TaskPriority.MEDIUM
    jurisdiction: Jurisdiction = Jurisdiction.BRASIL
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: dict[str, Any] | None = None
    error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentCapability(BaseModel):
    """Define uma capacidade do agente"""
    name: str
    description: str
    input_schema: dict[str, Any] = Field(default_factory=dict)
    output_schema: dict[str, Any] = Field(default_factory=dict)
    required_skills: list[str] = Field(default_factory=list)
    autonomy_level: AutonomyLevel = AutonomyLevel.A1_SUGGEST


class AgentConfig(BaseModel):
    """Configuração de um agente"""
    agent_id: str
    name: str
    layer: str
    description: str
    capabilities: list[AgentCapability] = Field(default_factory=list)
    autonomy_level: AutonomyLevel = AutonomyLevel.A1_SUGGEST
    jurisdictions: list[Jurisdiction] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    max_concurrent_tasks: int = 5
    timeout_seconds: int = 300
    retry_attempts: int = 3
    retry_delay_seconds: float = 1.0
    enabled: bool = True
    version: str = "1.0.0"
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentMetrics(BaseModel):
    """Métricas de performance do agente"""
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    total_processing_time: float = 0.0
    average_processing_time: float = 0.0
    last_activity: datetime | None = None
    uptime_seconds: float = 0.0
    success_rate: float = 0.0


class BaseAgent(ABC):
    """
    Classe base abstrata para todos os agentes do ecossistema Ventura.

    Implementa:
    - Ciclo de vida do agente
    - Gestão de tarefas
    - Governança e níveis de autonomia
    - Métricas e observabilidade
    - Integração futura com MCP (ver docs/MCP_FOR_AGENTS.md)
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self.settings = get_settings()
        self.status = AgentStatus.IDLE
        self.metrics = AgentMetrics()
        self._task_queue: asyncio.Queue[AgentTask] = asyncio.Queue()
        self._active_tasks: dict[str, AgentTask] = {}
        self._start_time = time.time()
        self._running = False
        self._initialized = False

    @property
    def agent_id(self) -> str:
        return self.config.agent_id

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def is_available(self) -> bool:
        return (
            self.config.enabled
            and self.status in (AgentStatus.IDLE, AgentStatus.PROCESSING)
            and len(self._active_tasks) < self.config.max_concurrent_tasks
        )

    # ==========================================
    # LIFECYCLE
    # ==========================================

    async def initialize(self) -> None:
        """Inicializa o agente e seus recursos"""
        logger.info(f"Initializing agent: {self.agent_id}")
        await self._on_initialize()
        self._initialized = True
        logger.info(f"Agent {self.agent_id} initialized successfully")

    async def start(self) -> None:
        """Inicia o loop de processamento do agente"""
        if not self._initialized:
            await self.initialize()

        self._running = True
        self.status = AgentStatus.IDLE
        logger.info(f"Agent {self.agent_id} started")

        # Inicia o loop de processamento
        asyncio.create_task(self._process_loop())

    async def stop(self) -> None:
        """Para o agente graciosamente"""
        logger.info(f"Stopping agent: {self.agent_id}")
        self._running = False

        # Aguarda tarefas ativas completarem
        if self._active_tasks:
            logger.info(f"Waiting for {len(self._active_tasks)} active tasks...")
            await asyncio.gather(
                *[self._wait_for_task(tid) for tid in list(self._active_tasks.keys())],
                return_exceptions=True,
            )

        await self._on_shutdown()
        self.status = AgentStatus.DISABLED
        logger.info(f"Agent {self.agent_id} stopped")

    # ==========================================
    # TASK MANAGEMENT
    # ==========================================

    async def submit_task(self, task: AgentTask) -> str:
        """Submete uma tarefa para o agente processar"""
        if not self.is_available:
            raise RuntimeError(
                f"Agent {self.agent_id} is not available. "
                f"Status: {self.status}, Active tasks: {len(self._active_tasks)}"
            )

        task.agent_id = self.agent_id
        await self._task_queue.put(task)
        logger.info(f"Task {task.id} submitted to agent {self.agent_id}")
        return task.id

    async def get_task_status(self, task_id: str) -> AgentTask | None:
        """Retorna o status de uma tarefa"""
        return self._active_tasks.get(task_id)

    async def cancel_task(self, task_id: str) -> bool:
        """Cancela uma tarefa ativa"""
        if task_id in self._active_tasks:
            task = self._active_tasks[task_id]
            task.error = "Cancelled by user"
            task.completed_at = datetime.now(UTC)
            del self._active_tasks[task_id]
            self.metrics.failed_tasks += 1
            return True
        return False

    # ==========================================
    # INTERNAL PROCESSING
    # ==========================================

    async def _process_loop(self) -> None:
        """Loop principal de processamento de tarefas"""
        while self._running:
            try:
                task = await asyncio.wait_for(
                    self._task_queue.get(), timeout=1.0
                )
                asyncio.create_task(self._execute_task(task))
            except TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error in process loop: {e}")
                await asyncio.sleep(1)

    async def _execute_task(self, task: AgentTask) -> None:
        """Executa uma tarefa com retry e governança"""
        self._active_tasks[task.id] = task
        task.started_at = datetime.now(UTC)
        self.status = AgentStatus.PROCESSING
        self.metrics.total_tasks += 1

        success = False
        for attempt in range(self.config.retry_attempts):
            try:
                # Verifica governança antes de executar
                if not await self._check_governance(task):
                    self.status = AgentStatus.WAITING_APPROVAL
                    logger.info(f"Task {task.id} waiting for approval")
                    approved = await self._wait_for_approval(task)
                    if not approved:
                        task.error = "Rejected by governance"
                        break

                # Executa a tarefa
                result = await asyncio.wait_for(
                    self._on_execute(task),
                    timeout=self.config.timeout_seconds,
                )

                task.result = result
                task.completed_at = datetime.now(UTC)
                self.metrics.completed_tasks += 1
                success = True

                # Callback de sucesso
                await self._on_task_success(task)
                break

            except TimeoutError:
                task.error = f"Timeout after {self.config.timeout_seconds}s (attempt {attempt + 1})"
                logger.warning(f"Task {task.id} timed out (attempt {attempt + 1})")
                if attempt < self.config.retry_attempts - 1:
                    await asyncio.sleep(self.config.retry_delay_seconds * (2 ** attempt))

            except Exception as e:
                task.error = str(e)
                logger.error(f"Task {task.id} failed (attempt {attempt + 1}): {e}")
                if attempt < self.config.retry_attempts - 1:
                    await asyncio.sleep(self.config.retry_delay_seconds * (2 ** attempt))

        if not success:
            self.metrics.failed_tasks += 1
            if task.completed_at is None:
                task.completed_at = datetime.now(UTC)
            await self._on_task_failure(task)

        # Cleanup e métricas
        if task.id in self._active_tasks:
            del self._active_tasks[task.id]

        if task.started_at and task.completed_at:
            duration = (task.completed_at - task.started_at).total_seconds()
            self.metrics.total_processing_time += duration
            if self.metrics.completed_tasks > 0:
                self.metrics.average_processing_time = (
                    self.metrics.total_processing_time / self.metrics.completed_tasks
                )

        self.metrics.last_activity = datetime.now(UTC)
        self.metrics.success_rate = (
            self.metrics.completed_tasks / max(self.metrics.total_tasks, 1)
        )
        self.metrics.uptime_seconds = time.time() - self._start_time

        if not self._active_tasks:
            self.status = AgentStatus.IDLE

    async def _wait_for_task(self, task_id: str) -> None:
        """Aguarda uma tarefa específica terminar"""
        while task_id in self._active_tasks:
            await asyncio.sleep(0.1)

    # ==========================================
    # GOVERNANCE
    # ==========================================

    async def _check_governance(self, task: AgentTask) -> bool:
        """
        Verifica se a tarefa pode ser executada com o nível de autonomia atual.
        Retorna True se pode executar, False se precisa de aprovação.
        """
        # Níveis A0 e A1 sempre precisam de aprovação
        if self.config.autonomy_level in (AutonomyLevel.A0_OBSERVE, AutonomyLevel.A1_SUGGEST):
            return False

        # A2+ pode executar, mas hard gates ainda aplicam
        if self.settings.hard_gates_enabled:
            amount = task.payload.get("amount", 0) or task.payload.get("value", 0)
            # Exemplo de hard gate: valores muito altos sempre requerem aprovação
            if isinstance(amount, (int, float)) and amount > 1_000_000:
                return False

        return True

    async def _wait_for_approval(self, task: AgentTask) -> bool:
        """
        Aguarda aprovação humana para a tarefa.

        Em desenvolvimento, auto-aprova para facilitar testes (ou quando o
        operador opta explicitamente por `hitl_auto_approve`). Em produção,
        falha de forma segura (fail-closed): sem um canal HITL configurado,
        a tarefa é rejeitada pela governança em vez de auto-aprovada.
        """
        logger.info(f"Approval requested for task {task.id} by agent {self.agent_id}")

        if self.settings.environment.value == "development" or self.settings.hitl_auto_approve:
            await asyncio.sleep(0.2)
            return True

        # TODO: Integrar com fila de aprovações / MCP human-loop.
        # Sem canal HITL, não auto-aprovar em produção.
        logger.warning(
            f"Task {task.id} rejected by governance: no human-in-the-loop channel configured "
            f"(environment={self.settings.environment.value})."
        )
        return False

    # ==========================================
    # ABSTRACT METHODS (devem ser implementados)
    # ==========================================

    @abstractmethod
    async def _on_initialize(self) -> None:
        """Hook de inicialização do agente específico"""
        ...

    @abstractmethod
    async def _on_execute(self, task: AgentTask) -> dict[str, Any]:
        """Executa a lógica principal da tarefa. Retorna o resultado."""
        ...

    @abstractmethod
    async def _on_shutdown(self) -> None:
        """Hook de shutdown do agente específico"""
        ...

    async def _on_task_success(self, task: AgentTask) -> None:
        """Callback opcional após sucesso da tarefa (pode ser sobrescrito)"""
        logger.info(f"Task {task.id} completed successfully by {self.agent_id}")

    async def _on_task_failure(self, task: AgentTask) -> None:
        """Callback opcional após falha da tarefa (pode ser sobrescrito)"""
        logger.error(f"Task {task.id} failed on {self.agent_id}: {task.error}")

    # ==========================================
    # OBSERVABILITY
    # ==========================================

    def health(self) -> dict[str, Any]:
        """Retorna estado de saúde do agente"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status.value,
            "enabled": self.config.enabled,
            "active_tasks": len(self._active_tasks),
            "queue_size": self._task_queue.qsize(),
            "metrics": self.metrics.model_dump(),
            "uptime_seconds": time.time() - self._start_time,
            "autonomy_level": self.config.autonomy_level.value,
            "layer": self.config.layer,
        }

    def get_capabilities(self) -> list[dict[str, Any]]:
        """Lista capacidades do agente"""
        return [cap.model_dump() for cap in self.config.capabilities]
