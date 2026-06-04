from typing import Any

from pydantic import BaseModel

from src.common.constants import ExceptionErrorMessages


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
        "description": "Error de validación en los datos de la petición.",
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
                    "message": ExceptionErrorMessages.REQUEST_DATA_INVALID.value,
                    "data": errors_example,
                },
            }
        },
    }


def response_scheme_401(
    jwt_auth_failed: bool = False,
    jwt_missing: bool = False,
    jwt_invalid: bool = False,
    jwt_expired: bool = False,
    jwt_user_not_found: bool = False,
) -> dict[str, Any]:
    """
    Genera un esquema de respuesta para errores **401** cuando se hace una solicitud no autorizada.
    """

    scheme: dict[str, Any] = {
        "description": "Solicitud no autorizada por algunos de los siguientes motivos.",
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

    if jwt_auth_failed:
        scheme["content"]["application/json"]["examples"]["jwt_auth"] = {
            "summary": "Credenciales invalidas",
            "value": {
                "success": False,
                "message": ExceptionErrorMessages.AUTHENTICATION_FAILED.value,
                "data": {},
            },
        }
    if jwt_missing:
        scheme["content"]["application/json"]["examples"]["jwt_missing"] = {
            "summary": "JWT faltante",
            "value": {
                "success": False,
                "message": ExceptionErrorMessages.JWT_MISSING.value,
                "data": {},
            },
        }
    if jwt_invalid:
        scheme["content"]["application/json"]["examples"]["invalid_jwt"] = {
            "summary": "JWT inválido",
            "value": {
                "success": False,
                "message": ExceptionErrorMessages.JWT_INVALID.value,
                "data": {},
            },
        }
    if jwt_expired:
        scheme["content"]["application/json"]["examples"]["expired_jwt"] = {
            "summary": "JWT expirado",
            "value": {
                "success": False,
                "message": ExceptionErrorMessages.JWT_EXPIRED.value,
                "data": {},
            },
        }
    if jwt_user_not_found:
        scheme["content"]["application/json"]["examples"]["user_not_found"] = {
            "summary": "JWT usuario no encontrado",
            "value": {
                "success": False,
                "message": ExceptionErrorMessages.JWT_USER_NOT_FOUND.value,
                "data": {},
            },
        }

    return scheme


def response_scheme_404() -> dict[str, Any]:
    """Genera un esquema de respuesta para errores **404**."""

    return {
        "description": "Recurso no encontrado.",
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
                "example": {
                    "success": False,
                    "message": ExceptionErrorMessages.RESOURCE_NOT_FOUND.value,
                    "data": {},
                },
            }
        },
    }


def response_scheme_403() -> dict[str, Any]:
    """Genera un esquema de respuesta para errores **403**."""

    return {
        "description": "Acceso denegado.",
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
                "example": {
                    "success": False,
                    "message": ExceptionErrorMessages.PERMISSION_DENIED.value,
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
                "message": ExceptionErrorMessages.DB_UNAVAILABLE.value,
                "data": {},
            },
        }

    return scheme
