import logging

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "BridgeStack API"
    app_version: str = "0.3.0"
    app_description: str = "API backend bridging OpenStacks data layers"
    database_url: str = "sqlite:///./rootstack.db"
    debug: bool = False
    cors_origins: list[str] = ["*"]
    log_level: str = "INFO"

    model_config = {"env_prefix": "BRIDGE_"}


settings = Settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("bridgestack")
