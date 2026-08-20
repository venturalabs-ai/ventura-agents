"""
Ventura Labs AI - Configuração Central
Versão: 3.0.0
"""

from __future__ import annotations

import os
from enum import StrEnum
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Jurisdiction(StrEnum):
    BRASIL = "BR"
    EUA = "US"
    UNIAO_EUROPEIA = "EU"
    CHINA = "CN"
    INDIA = "IN"


class AutonomyLevel(StrEnum):
    """Níveis de autonomia dos agentes (A0-A4)"""

    A0_OBSERVE = "A0"  # Apenas observa e reporta
    A1_SUGGEST = "A1"  # Sugere ações, humano decide
    A2_APPROVE = "A2"  # Executa com aprovação prévia
    A3_AUTONOMOUS = "A3"  # Autônomo com limites
    A4_FULL = "A4"  # Autonomia total (raro)


class Settings(BaseSettings):
    """Configurações da aplicação"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_name: str = "Ventura Agents Ecosystem"
    app_version: str = "3.0.0"
    environment: Environment = Environment.DEVELOPMENT
    debug: bool = Field(default=False)

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/ventura_agents"
    )
    redis_url: str = Field(default="redis://localhost:6379/0")

    # Vector Database (RAG)
    vector_db_type: str = "chromadb"  # chromadb, pinecone, weaviate, qdrant
    vector_db_url: str = Field(default="http://localhost:8080")
    vector_db_collection: str = "ventura_knowledge"
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536

    # LLM Configuration
    llm_provider: str = "openai"  # openai, anthropic, azure
    llm_model: str = "gpt-4o"
    llm_api_key: str = Field(default="", alias="LLM_API_KEY")
    llm_temperature: float = 0.1
    llm_max_tokens: int = 4096

    # Context Compression
    compression_enabled: bool = True
    compression_ratio_target: float = 0.10  # 90% reduction
    compression_strategy: str = "hierarchical"  # hierarchical, semantic, hybrid

    # MCP (Model Context Protocol)
    mcp_enabled: bool = True
    mcp_transport: str = "stdio"  # stdio, sse, websocket
    mcp_server_host: str = "localhost"
    mcp_server_port: int = 3001

    # Governance
    default_autonomy_level: AutonomyLevel = AutonomyLevel.A1_SUGGEST
    max_autonomy_level: AutonomyLevel = AutonomyLevel.A3_AUTONOMOUS
    require_approval_above: AutonomyLevel = AutonomyLevel.A2_APPROVE
    hard_gates_enabled: bool = True
    # Opt-in auto-approval outside development. Default False keeps governance fail-closed.
    hitl_auto_approve: bool = False

    # Observability
    otel_enabled: bool = True
    otel_endpoint: str = Field(default="http://localhost:4317")
    otel_service_name: str = "ventura-agents"
    log_level: str = "INFO"
    log_format: str = "json"

    # Multi-Jurisdiction
    default_jurisdiction: Jurisdiction = Jurisdiction.BRASIL
    enabled_jurisdictions: list[Jurisdiction] = [
        Jurisdiction.BRASIL,
        Jurisdiction.EUA,
        Jurisdiction.UNIAO_EUROPEIA,
    ]

    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds

    # Security
    jwt_secret: str = Field(default="change-me-in-production", alias="JWT_SECRET")
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600

    @field_validator("llm_api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        if not v and os.environ.get("ENVIRONMENT") == "production":
            raise ValueError("LLM_API_KEY is required in production")
        return v

    @field_validator("jwt_secret")
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        if v == "change-me-in-production" and os.environ.get("ENVIRONMENT") == "production":
            raise ValueError("JWT_SECRET must be changed in production")
        return v


@lru_cache
def get_settings() -> Settings:
    """Retorna instância singleton das configurações"""
    return Settings()
