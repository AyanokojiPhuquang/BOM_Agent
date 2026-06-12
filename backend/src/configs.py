import logging
import os

from pydantic_settings import BaseSettings, SettingsConfigDict

# Suppress harmless "Failed to detach context" warnings from OpenTelemetry.
# These occur when Langfuse's OTel context propagation crosses async boundaries
# (e.g. LangGraph graph.ainvoke/astream). The detach failure is cosmetic —
# trace data is still captured correctly.
logging.getLogger("opentelemetry.context").setLevel(logging.CRITICAL)


class SMTPConfig(BaseSettings):
    server: str = ""
    port: int = 587
    username: str = ""
    password: str = ""


class DatabaseConfig(BaseSettings):
    url: str = "postgresql+asyncpg://starlink:starlink@localhost:5432/starlink"
    echo: bool = False


class AuthConfig(BaseSettings):
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


class Settings(BaseSettings):
    env: str = "development"
    database: DatabaseConfig = DatabaseConfig()
    checkpoint_db_url: str = "postgresql://starlink:starlink@localhost:5432/starlink"
    auth: AuthConfig = AuthConfig()
    smtp: SMTPConfig = SMTPConfig()
    escalation_email: str = ""
    bom_recipient_email: str = ""
    openai_api_key: str = ""
    openai_api_base_url: str = "https://api.openai.com/v1"
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_base_url: str = "https://cloud.langfuse.com"
    cors_origins: str = "http://localhost:5173"
    datasheets_dir: str = "data/datasheets"

    # Google Drive OAuth
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8030/api/drive/auth/callback"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Token encryption (Fernet key)
    token_encryption_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
        env_nested_delimiter="__",
        env_nested_max_split=1,
    )


SETTINGS = Settings()

# Set environment variables for downstream libraries
if SETTINGS.openai_api_key:
    os.environ["OPENAI_API_KEY"] = SETTINGS.openai_api_key

os.environ["LANGFUSE_PUBLIC_KEY"] = SETTINGS.langfuse_public_key
os.environ["LANGFUSE_SECRET_KEY"] = SETTINGS.langfuse_secret_key
os.environ["LANGFUSE_HOST"] = SETTINGS.langfuse_base_url
os.environ["LANGFUSE_TRACING_ENVIRONMENT"] = SETTINGS.env
