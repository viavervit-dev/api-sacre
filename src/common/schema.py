from typing import Any

from pydantic import BaseModel


def build_response_scheme_400(dto_class: type[BaseModel]) -> dict[str, Any]:
    """
    Genera un esquema de respuesta para errores **400** basado en las validaciones definidas
    en el DTO de la solicitud.
    """

    errors_example = {}
    data_properties = {}

    for field_name, field_class in dto_class.model_fields.items():
        error_list = field_class.json_schema_extra["x-validation-errors"]  # type: ignore

        errors_example[field_name] = error_list
        data_properties[field_name] = {
            "type": "array",
            "items": {"type": "string"},
        }

    return {
        "description": "Error de validación en los datos enviados.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "message": {"type": "string"},
                        "data": {
                            "type": "object",
                            "properties": data_properties,
                        },
                    },
                },
                "example": {
                    "success": False,
                    "message": "Error de validación en los datos enviados.",
                    "data": errors_example,
                },
            }
        },
    }


def build_response_scheme_503(db_unavailable: bool) -> dict[str, Any]:
    """
    Genera un esquema de respuesta para errores **503** cuando algún componente de la API
    no está disponible.
    """

    scheme: dict[str, Any] = {
        "description": "Algún componente de la API no está disponible.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "message": {"type": "string"},
                        "data": {"type": "object"},
                    },
                },
                "examples": {},
            }
        },
    }

    if db_unavailable:
        scheme["content"]["application/json"]["examples"]["db_unavailable"] = {
            "summary": "Base de datos",
            "value": {
                "success": False,
                "message": "El servicio de base de datos no está disponible.",
                "data": {},
            },
        }

    return scheme
