from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[3]
AI_ENGINE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    project_name: str = "SmartRecycleAI"
    environment: str = "development"
    ai_engine_host: str = "0.0.0.0"
    ai_engine_port: int = 8100
    ai_model_path: str = "models/yolov8n.pt"

    model_config = SettingsConfigDict(
        env_file=(ROOT_DIR / ".env", AI_ENGINE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def model_path(self) -> Path:
        path = Path(self.ai_model_path)
        return path if path.is_absolute() else AI_ENGINE_DIR / path


@lru_cache
def get_settings() -> Settings:
    return Settings()
