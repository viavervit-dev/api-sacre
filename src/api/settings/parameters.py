import tomllib
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_app_version() -> str:
    """Lee la versión directamente del archivo `pyproject.toml`."""

    pyproject_path = Path(__file__).resolve().parents[3] / "pyproject.toml"

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


class ApiParameters(BaseSettings):
    """
    Clase de configuración para los parámetros de la API. Esta clase utiliza Pydantic para
    validar y cargar automáticamente las variables de entorno definidas en un archivo `.env`.
    """

    model_config = SettingsConfigDict(
        env_file="src/.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Aplicación
    app_name: str = "API Sacre"
    app_version: str = Field(default_factory=get_app_version)
    pagination_limit: int = 50
    debug: bool

    # Base de Datos
    alembic_database_url: str | None = None
    database_url: str
    db_pool_size: int
    db_pool_max_overflow: int
    db_pool_timeout: int
    db_pool_recycle: int
    db_echo: bool
    db_command_timeout: int
    db_jit: str
    db_statement_timeout: str

    # Seguridad
    private_key: str
    public_key: str
    jwt_algorithm: str = "EdDSA"
    access_token_expire: int = 15  # 15 minutos
    refresh_token_expire: int = 5760  # 4 días

    # Servidor
    host: str
    port: int
    workers: int


@lru_cache
def get_api_parameters() -> ApiParameters:
    """
    Carga y devuelve los parámetros de la API desde el archivo `.env`. Utiliza caching para
    evitar recargar los parámetros en cada llamada.
    """

    return ApiParameters()  # type: ignore[call-arg]  # pyright: ignore[reportCallIssue]


api_parameters = get_api_parameters()
