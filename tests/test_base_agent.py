import pytest

from agents.base.agent import AgentConfig, AgentTask, BaseAgent
from core.config import AutonomyLevel, Environment, Settings


class _EchoAgent(BaseAgent):
    async def _on_initialize(self) -> None:
        return None

    async def _on_execute(self, task: AgentTask) -> dict[str, object]:
        return {"echo": task.payload}

    async def _on_shutdown(self) -> None:
        return None


class _FailAgent(BaseAgent):
    async def _on_initialize(self) -> None:
        return None

    async def _on_execute(self, task: AgentTask) -> dict[str, object]:
        raise RuntimeError("boom")

    async def _on_shutdown(self) -> None:
        return None


@pytest.fixture
def make_agent(monkeypatch):
    def factory(cls=_EchoAgent, settings=None, **config_overrides):
        if settings is None:
            settings = Settings(_env_file=None)
        monkeypatch.setattr("agents.base.agent.get_settings", lambda: settings)
        config = AgentConfig(
            agent_id="test-agent",
            name="Test Agent",
            layer="test",
            description="test agent",
            **config_overrides,
        )
        return cls(config)

    return factory


def test_health_reports_metrics(make_agent):
    agent = make_agent()
    health = agent.health()
    assert health["agent_id"] == "test-agent"
    assert health["status"] == "idle"
    assert health["metrics"]["total_tasks"] == 0


async def test_governance_requires_approval_for_a1(make_agent):
    agent = make_agent(autonomy_level=AutonomyLevel.A1_SUGGEST)
    task = AgentTask(task_type="x", payload={})
    assert not await agent._check_governance(task)


async def test_hard_gate_blocks_large_amounts(make_agent):
    agent = make_agent(autonomy_level=AutonomyLevel.A3_AUTONOMOUS)
    blocked = AgentTask(task_type="x", payload={"amount": 2_000_000})
    allowed = AgentTask(task_type="x", payload={"amount": 500_000})
    assert not await agent._check_governance(blocked)
    assert await agent._check_governance(allowed)


async def test_wait_for_approval_auto_approves_in_development(make_agent):
    agent = make_agent()
    task = AgentTask(task_type="x", payload={})
    assert await agent._wait_for_approval(task)


async def test_wait_for_approval_fails_closed_in_production(make_agent):
    agent = make_agent(settings=Settings(_env_file=None, environment=Environment.PRODUCTION))
    task = AgentTask(task_type="x", payload={})
    assert not await agent._wait_for_approval(task)


async def test_wait_for_approval_opt_in_in_production(make_agent):
    settings = Settings(_env_file=None, environment=Environment.PRODUCTION, hitl_auto_approve=True)
    agent = make_agent(settings=settings)
    task = AgentTask(task_type="x", payload={})
    assert await agent._wait_for_approval(task)


async def test_successful_execution_updates_metrics(make_agent):
    agent = make_agent(autonomy_level=AutonomyLevel.A3_AUTONOMOUS)
    task = AgentTask(task_type="x", payload={"amount": 100})
    await agent._execute_task(task)
    assert agent.metrics.completed_tasks == 1
    assert agent.metrics.failed_tasks == 0
    assert agent.metrics.success_rate == 1.0
    assert task.result == {"echo": {"amount": 100}}


async def test_execute_task_retries_and_records_failure(make_agent):
    agent = make_agent(cls=_FailAgent, retry_attempts=2, retry_delay_seconds=0)
    task = AgentTask(task_type="x", payload={})
    await agent._execute_task(task)
    assert agent.metrics.total_tasks == 1
    assert agent.metrics.failed_tasks == 1
    assert task.error == "boom"


async def test_rejected_governance_marks_task_failed(make_agent):
    settings = Settings(_env_file=None, environment=Environment.PRODUCTION)
    agent = make_agent(settings=settings, autonomy_level=AutonomyLevel.A1_SUGGEST)
    task = AgentTask(task_type="x", payload={})
    await agent._execute_task(task)
    assert task.error == "Rejected by governance"
    assert agent.metrics.failed_tasks == 1
