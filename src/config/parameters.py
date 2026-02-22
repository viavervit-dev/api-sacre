import tomllib
from functools import lru_cache
from pathlib import Path

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_app_version() -> str:
    """Lee la versión directamente del archivo `pyproject.toml`."""

    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"

    if not pyproject_path.exists():
        raise FileNotFoundError(f"pyproject.toml not found at: {pyproject_path}")

    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    try:
        return data["tool"]["poetry"]["version"]
    except KeyError as e:
        raise ValueError(
            "Version not found in pyproject.toml. "
            "Ensure [tool.poetry] section contains 'version' field."
        ) from e


class Settings(BaseSettings):
    """
    Configuración de la aplicación.

    Todas las configuraciones se cargan desde variables de entorno. Las variables requeridas deben
    estar definidas o la aplicación fallará al iniciar.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # === Aplicación ===
    app_name: str
    app_version: str = Field(default_factory=get_app_version)
    debug: bool

    # === Base de Datos ===
    database_url: PostgresDsn
    db_pool_size: int = Field(ge=1, le=100)
    db_pool_max_overflow: int = Field(ge=0, le=100)

    # === Seguridad ===
    secret_key: str = Field(min_length=32)

    # === Servidor ===
    host: str
    port: int
    workers: int = Field(ge=1, le=32)


@lru_cache
def get_settings() -> Settings:
    """
    Obtiene una instancia cacheada de la configuración. Usa `lru_cache` para evitar releer las
    variables de entorno en cada acceso a la configuración.
    """

    return Settings()  # type: ignore[call-arg]  # pyright: ignore[reportCallIssue]


settings = get_settings()
