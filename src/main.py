from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import APIRouter, Depends, FastAPI
from fastapi import Response as FastAPIResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.response import Response
from src.config.database import check_db_connection, close_db_pool, create_db_pool, get_db_session
from src.config.exception_handlers import register_exception_handlers
from src.config.parameters import settings
from src.config.serialization import JSONResponse
from src.modules.customers.repositories.customer import CustomerCreateDTO, CustomerRepository


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Gestor del ciclo de vida de la aplicación, maneja los eventos de inicio y cierre:
    - **Inicio:** Inicializa la piscina de conexiones a la base de datos.
    - **Cierre:** Cierra las conexiones de forma segura.
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


# Registra los manejadores de excepciones personalizados
register_exception_handlers(app=app)


# Configura el router principal para la API, con un prefijo para todas las rutas v1
v1_router = APIRouter(prefix="/api/v1")
app.include_router(router=v1_router)


class HealthCheck(BaseModel):
    """Modelo de respuesta para el endpoint de verificación de salud."""

    database: str = Field(description="Estado de la conexión a la base de datos.")


@app.get(
    path="/health/",
    responses={
        200: {
            "description": "Todos los componentes de la API están disponibles.",
            "model": Response[HealthCheck],
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Todos los componentes de la API están disponibles.",
                        "data": {"database": "healthy"},
                    },
                }
            },
        },
        503: {
            "description": "Algún componente de la API no está disponible.",
            "model": Response[HealthCheck],
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "Algún componente de la API no está disponible.",
                        "data": {"database": "unhealthy"},
                    },
                }
            },
        },
    },
)
async def health_check(
    response: FastAPIResponse,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> Response[HealthCheck]:
    """Endpoint de verificación de salud para balanceadores de carga y monitoreo."""

    data = CustomerCreateDTO(
        email="prueba_manual@foo.com",
        password="ClaveFuerte1",
        first_names="Lionel",
        last_names="Messi",
        document_type="RUT",
        document_number="12312312",
        phone="+549112223344",
    )

    customer = await CustomerRepository.create_customer(data=data, session=session)
    print(customer)

    response.status_code = 200
    checks = {"database": "healthy"}
    healthy = True

    if not await check_db_connection():
        checks["database"] = "unhealthy"
        healthy = False

    if not healthy:
        response.status_code = 503

    return Response(
        success=healthy,
        message="Estado de salud de la API.",
        data=HealthCheck(**checks),
    )


if __name__ == "__main__":
    uvicorn.run(
        app="src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
