from enum import IntEnum
from pydantic_settings import BaseSettings
from sqlalchemy import MetaData

class EnvironmentMode(IntEnum):
    DEVELOPMENT = 0
    STAGING = 1
    PRODUCTION = 2

class Settings(BaseSettings):

    OAUTH2_URL: str = ""
    OAUTH2_TOKEN: str = ""
    DB_CONFIG: str = ""
    OAUTH_ROLE: str = 'PROJECT_USER'
    IS_STAGING: bool = True
    QUEUE_LOCATION: str
    PROJECT_NAME: str
    POSTGRES_SCHEMA: str
    RABBITMQ_EXCHANGE_NAME: str
    RABBITMQ_BASE_URL: str
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    RABBITMQ_VHOST: str
    EXPECTED_AUDIENCE: str
    EXPECTED_SA_EMAIL: str

    ENV_MODE: int = 0

    #Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    #OpenTelemetry
    OTEL_EXPORTER_OTLP_ENDPOINT: str
    OTEL_SERVICE_NAME: str
    OTEL_SERVICE_VERSION: str

    INTERNAL_API_KEY: str
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

# SETUP MODEL METADATA
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
model_metadata = MetaData(schema=settings.POSTGRES_SCHEMA, naming_convention=naming_convention)
