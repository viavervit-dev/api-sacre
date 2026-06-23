from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi import Response as FastAPIResponse
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field

from src.common.response import Response
from src.config.database import check_db_connection, close_db_pool, create_db_pool
from src.config.exception_handlers import register_exception_handlers
from src.config.parameters import settings
from src.config.serialization import JSONResponse
from src.modules.auth.routers.jwt.authenticate_admin import router as jwt_login_admin
from src.modules.customers.routers.create import router as create_customer
from src.modules.products.routers.create_category import router as get_category
from src.modules.products.routers.create_prodcut import router as create_prodcut
from src.modules.products.routers.delete_category import router as delete_category
from src.modules.products.routers.delete_product import router as delete_product
from src.modules.products.routers.get_category import router as create_category
from src.modules.products.routers.get_product import router as get_product
from src.modules.products.routers.update_category import router as update_category
from src.modules.products.routers.update_product import router as update_product


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


def openapi() -> dict[str, Any]:
    """
    Genera el esquema OpenAPI personalizado para la aplicación, eliminando el código de
    estado 422 de las respuestas.
    """

    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    # Eliminar el 422 de todos los endpoints
    for path in schema.get("paths", {}).values():
        for operation in path.values():
            operation.get("responses", {}).pop("422", None)

    app.openapi_schema = schema

    return app.openapi_schema


app.openapi = openapi  # type: ignore[method-assign]


# Registra los manejadores de excepciones personalizados
register_exception_handlers(app=app)


# Configura el router principal para la API, con un prefijo para todas las rutas v1
v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(router=create_customer)
v1_router.include_router(router=jwt_login_admin)
v1_router.include_router(router=get_category)
v1_router.include_router(router=create_category)
v1_router.include_router(router=update_category)
v1_router.include_router(router=get_product)
v1_router.include_router(router=create_prodcut)
v1_router.include_router(router=update_product)
v1_router.include_router(router=delete_product)
v1_router.include_router(router=delete_category)
app.include_router(router=v1_router)


class HealthCheck(BaseModel):
    """Modelo de respuesta para el endpoint de verificación de salud."""

    database: str = Field(description="Estado de la conexión a la base de datos.")


@app.get(
    path="/health/",
    tags=["Utilidades"],
    responses={
        200: {
            "description": "**(OK)** Estado de salud de los componentes de la API.",
            "model": Response[HealthCheck],
            "content": {
                "application/json": {
                    "examples": {
                        "available": {
                            "summary": "Disponibles",
                            "value": {
                                "success": True,
                                "pagination": False,
                                "message": "Todos los componentes de la API están disponibles.",
                                "data": {"database": "healthy"},
                            },
                        },
                        "unavailable": {
                            "summary": "No disponibles",
                            "value": {
                                "success": True,
                                "pagination": False,
                                "message": "Algunos componentes de la API no están disponibles.",
                                "data": {"database": "unhealthy"},
                            },
                        },
                    },
                }
            },
        },
    },
)
async def health_check(response: FastAPIResponse) -> Response[HealthCheck]:
    """Endpoint de verificación de salud para balanceadores de carga y monitoreo."""

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
        pagination=False,
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
