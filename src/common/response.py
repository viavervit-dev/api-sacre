from typing import TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Response[T](BaseModel):
    """Respuesta estándar para todos los endpoints."""

    success: bool = Field(description="Indica si la operación fue exitosa.")
    message: str = Field(description="Mensaje descriptivo sobre el resultado de la petición.")
    data: T = Field(description="Payload de la respuesta.")
