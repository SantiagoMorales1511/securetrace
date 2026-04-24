from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SecureTrace API"
    app_version: str = "0.1.0"
    debug: bool = True

    database_url: str = "sqlite:///./securetrace.db"

    cors_allow_origins: list[str] = ["http://localhost:5173"]
    repository_clone_dir: str = "./.repositories_cache"
    git_clone_timeout_sec: int = 120

    repository_excluded_dirs: list[str] = [
        ".git",
        ".idea",
        ".vscode",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
        ".venv",
        "venv",
    ]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
