from typing import TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Response[T](BaseModel):
    """Respuesta estándar para todos los endpoints."""

    success: bool = Field(description="Indica si la operación fue exitosa.")
    pagination: bool = Field(description="Indica si la respuesta incluye datos paginados.")
    message: str = Field(description="Mensaje descriptivo sobre el resultado de la petición.")
    data: T = Field(description="Payload de la respuesta.")


class PaginationMeta(BaseModel):
    """Metadatos necesarios para respuestas con paginación."""

    total: int = Field(description="Total absoluto de registros que coinciden con los filtros.")
    offset: int = Field(description="Registros saltados en esta página.")
    limit: int = Field(description="Límite de registros solicitados.")


class PaginatedData[T](BaseModel):
    """Estructura del payload para respuestas con paginación."""

    items: list[T] = Field(description="Lista de registros de la página actual.")
    meta: PaginationMeta = Field(description="Información de la paginación.")
