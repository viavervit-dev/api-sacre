import tomllib
from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_app_version() -> str:
    """Lee la versión directamente del archivo `pyproject.toml` con fallback seguro."""

    pyproject_path = Path(__file__).resolve().parents[3] / "pyproject.toml"

    if pyproject_path.exists():
        try:
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
            return str(data.get("tool", {}).get("poetry", {}).get("version", "0.1.0"))
        except Exception:
            pass

    try:
        from importlib.metadata import version

        return version("api-sacre")
    except Exception:
        return "0.1.0"


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
    enable_docs: bool
    cors_origins: str

    # Base de Datos
    alembic_database_url: str
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
    access_token_expire: int
    refresh_token_expire: int

    # Gestor de pagos
    api_payment_links: str
    api_payment_key: str
    api_payment_store_id: str

    # Correo Electrónico (SMTP)
    mail_username: str
    mail_password: str
    mail_from_address: str
    mail_server: str
    mail_port: int
    mail_use_ssl: bool
    mail_starttls: bool
    mail_timeout: int

    # Servidor
    host: str
    port: int
    workers: int
    forwarded_allow_ips: str

    @field_validator("private_key", "public_key", mode="before")
    @classmethod
    def normalize_pem_key(cls, v: str) -> str:
        """Normaliza cadenas PEM reemplazando saltos de línea escapados si existen."""

        if isinstance(v, str):
            v = v.strip().strip("'\"")

            if "\\n" in v:
                v = v.replace("\\n", "\n")

        return v

    @property
    def cors_origins_list(self) -> list[str]:
        """Devuelve la lista de orígenes permitidos para CORS."""

        if not self.cors_origins:
            return []

        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def is_docs_enabled(self) -> bool:
        """Determina si la documentación Swagger/OpenAPI debe exponerse."""

        if self.enable_docs is not None:
            return self.enable_docs

        return self.debug


@lru_cache
def get_api_parameters() -> ApiParameters:
    """
    Carga y devuelve los parámetros de la API desde el archivo `.env`. Utiliza caching para
    evitar recargar los parámetros en cada llamada.
    """

    return ApiParameters()  # type: ignore[call-arg]  # pyright: ignore[reportCallIssue]


api_parameters = get_api_parameters()
