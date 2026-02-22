from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.database import close_db_pool, create_db_pool
from src.config.exception_handlers import register_exception_handlers
from src.config.parameters import settings
from src.config.serialization import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Gestor del ciclo de vida de la aplicación.

    Maneja los eventos de inicio y cierre:
    - Inicio: Inicializa la piscina de conexiones a la base de datos.
    - Cierre: Cierra las conexiones de forma segura.
    """

    # Inicio
    await create_db_pool()
    yield
    # Cierre
    await close_db_pool()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
    default_response_class=JSONResponse,
)

register_exception_handlers(app)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Endpoint de verificación de salud para balanceadores de carga y monitoreo."""

    return {"status": "healthy"}
