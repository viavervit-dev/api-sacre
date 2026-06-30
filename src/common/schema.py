from typing import Any

from pydantic import BaseModel

from src.common.constants import ExceptionErrorMessages as CommonExceptionErrorMessages
from src.modules.auth.constants import ExceptionErrorMessages as AuthExceptionErrorMessages
from src.modules.inventory.constants import (
    ExceptionErrorMessages as InventoryExceptionErrorMessages,
)


def response_scheme_400(dto_class: type[BaseModel]) -> dict[str, Any]:
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
        "description": "**(BAD_REQUEST)** Error de validación en los datos de la petición.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "pagination": {"type": "boolean"},
                        "message": {"type": "string"},
                        "data": {
                            "type": "object",
                            "properties": data_properties,
                        },
                    },
                },
                "example": {
                    "success": False,
                    "pagination": False,
                    "message": CommonExceptionErrorMessages.REQUEST_DATA_INVALID.value,
                    "data": errors_example,
                },
            }
        },
    }


def response_scheme_401(
    jwt_auth_failed: bool = False,
    access_jwt_missing: bool = False,
    refresh_jwt_missing: bool = False,
    access_jwt_invalid: bool = False,
    refresh_jwt_invalid: bool = False,
    jwt_user_not_found: bool = False,
    category_has_dependencies: bool = False,
    product_has_reserved_stock: bool = False,
) -> dict[str, Any]:
    """
    Genera un esquema de respuesta para errores **401** cuando se hace una solicitud no autorizada.
    """

    scheme: dict[str, Any] = {
        "description": "**(UNAUTHORIZED)** Solicitud no autorizada por algunos de los siguientes "
        "motivos.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "pagination": {"type": "boolean"},
                        "message": {"type": "string"},
                        "data": {"type": "object"},
                    },
                },
                "examples": {},
            }
        },
    }

    if jwt_auth_failed:
        scheme["content"]["application/json"]["examples"]["jwt_auth"] = {
            "summary": "JWT - Credenciales invalidas",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionErrorMessages.CREDENTIALS_INVALID.value,
                "data": {},
            },
        }
    if access_jwt_missing:
        scheme["content"]["application/json"]["examples"]["access_jwt_missing"] = {
            "summary": "JWT - Falta de Token de acceso en Cookie",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionErrorMessages.ACCESS_JWT_MISSING.value,
                "data": {},
            },
        }
    if refresh_jwt_missing:
        scheme["content"]["application/json"]["examples"]["refresh_jwt_missing"] = {
            "summary": "JWT - Falta de Token de actualización en Cookie",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionErrorMessages.REFRESH_JWT_MISSING.value,
                "data": {},
            },
        }
    if access_jwt_invalid:
        scheme["content"]["application/json"]["examples"]["access_jwt_invalid"] = {
            "summary": "JWT - Token de acceso inválido",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionErrorMessages.ACCESS_JWT_INVALID.value,
                "data": {},
            },
        }
        scheme["content"]["application/json"]["examples"]["access_jwt_expired"] = {
            "summary": "JWT - Token de acceso expirado",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionErrorMessages.ACCESS_JWT_EXPIRED.value,
                "data": {},
            },
        }
    if refresh_jwt_invalid:
        scheme["content"]["application/json"]["examples"]["refresh_jwt_invalid"] = {
            "summary": "JWT - Token de actualización inválido",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionErrorMessages.REFRESH_JWT_INVALID.value,
                "data": {},
            },
        }
        scheme["content"]["application/json"]["examples"]["refresh_jwt_expired"] = {
            "summary": "JWT - Token de actualización expirado",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionErrorMessages.REFRESH_JWT_EXPIRED.value,
                "data": {},
            },
        }
    if jwt_user_not_found:
        scheme["content"]["application/json"]["examples"]["jwt_user_not_found"] = {
            "summary": "JWT - Usuario del token de acceso no existe",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionErrorMessages.JWT_USER_NOT_FOUND.value,
                "data": {},
            },
        }
    if category_has_dependencies:
        scheme["content"]["application/json"]["examples"]["category_has_dependencies"] = {
            "summary": "Violación de regla de dominio",
            "value": {
                "success": False,
                "pagination": False,
                "message": InventoryExceptionErrorMessages.CATEGORY_HAS_DEPENDENCIES.value,
                "data": {},
            },
        }
    if product_has_reserved_stock:
        scheme["content"]["application/json"]["examples"]["product_has_reserved_stock"] = {
            "summary": "Violación de regla de dominio",
            "value": {
                "success": False,
                "pagination": False,
                "message": InventoryExceptionErrorMessages.PRODUCT_HAS_RESERVED_STOCK.value,
                "data": {},
            },
        }

    return scheme


def response_scheme_404() -> dict[str, Any]:
    """Genera un esquema de respuesta para errores **404**."""

    return {
        "description": "**(NOT_FOUND)** Recurso no encontrado.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "pagination": {"type": "boolean"},
                        "message": {"type": "string"},
                        "data": {"type": "object"},
                    },
                },
                "example": {
                    "success": False,
                    "pagination": False,
                    "message": CommonExceptionErrorMessages.RESOURCE_NOT_FOUND.value,
                    "data": {},
                },
            }
        },
    }


def response_scheme_403() -> dict[str, Any]:
    """Genera un esquema de respuesta para errores **403**."""

    return {
        "description": "**(FORBIDDEN)** Acceso denegado.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "pagination": {"type": "boolean"},
                        "message": {"type": "string"},
                        "data": {"type": "object"},
                    },
                },
                "example": {
                    "success": False,
                    "pagination": False,
                    "message": AuthExceptionErrorMessages.PERMISSION_DENIED.value,
                    "data": {},
                },
            }
        },
    }


def response_scheme_503(db_unavailable: bool = False) -> dict[str, Any]:
    """
    Genera un esquema de respuesta para errores **503** cuando algún componente de la API
    no está disponible.
    """

    scheme: dict[str, Any] = {
        "description": "**(SERVICE_UNAVAILABLE)** Algún componente de la API no está disponible.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "pagination": {"type": "boolean"},
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
                "pagination": False,
                "message": CommonExceptionErrorMessages.DB_UNAVAILABLE.value,
                "data": {},
            },
        }

    return scheme
