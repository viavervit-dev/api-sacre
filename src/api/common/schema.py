from typing import Any

from pydantic import BaseModel

from src.api.common.email.constants import ExceptionErrorMessages as EmailException
from src.api.common.exceptions import ExceptionErrorMessages as CommonException
from src.api.modules.auth.constants import ExceptionErrorMessages as AuthExceptionError
from src.api.modules.inventory.constants import ExceptionErrorMessages as InventoryException
from src.api.modules.payments.constants import ExceptionErrorMessages as PaymentException


def response_scheme_400(dto_class: type[BaseModel]) -> dict[str, Any]:
    """Genera el esquema OpenAPI de error 400 (Bad Request) según el DTO proporcionado."""

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
                    "message": CommonException.REQUEST_DATA_INVALID.value,
                    "data": errors_example,
                },
            }
        },
    }


def response_scheme_401(
    credentials_invalid: bool = False,
    auth_session_expired: bool = False,
    access_jwt_missing: bool = False,
    refresh_jwt_missing: bool = False,
    access_jwt_invalid: bool = False,
    refresh_jwt_invalid: bool = False,
    access_jwt_expired: bool = False,
    access_jwt_not_expired: bool = False,
    refresh_jwt_expired: bool = False,
    jwt_user_not_found: bool = False,
) -> dict[str, Any]:
    """Genera el esquema OpenAPI de error 401 (Unauthorized) con ejemplos condicionales."""

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

    if credentials_invalid:
        scheme["content"]["application/json"]["examples"]["credentials_invalid"] = {
            "summary": "JWT - Credenciales invalidas",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionError.CREDENTIALS_INVALID.value,
                "data": {},
            },
        }
    if auth_session_expired:
        scheme["content"]["application/json"]["examples"]["auth_session_expired"] = {
            "summary": "JWT - Sesión inválida o ha expirado",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionError.AUTH_SESSION_EXPIRED.value,
                "data": {},
            },
        }
    if access_jwt_missing:
        scheme["content"]["application/json"]["examples"]["access_jwt_missing"] = {
            "summary": "JWT - Falta de Token de acceso en Cookie",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionError.ACCESS_JWT_MISSING.value,
                "data": {},
            },
        }
    if refresh_jwt_missing:
        scheme["content"]["application/json"]["examples"]["refresh_jwt_missing"] = {
            "summary": "JWT - Falta de Token de actualización en Cookie",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionError.REFRESH_JWT_MISSING.value,
                "data": {},
            },
        }
    if access_jwt_invalid:
        scheme["content"]["application/json"]["examples"]["access_jwt_invalid"] = {
            "summary": "JWT - Token de acceso inválido",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionError.ACCESS_JWT_INVALID.value,
                "data": {},
            },
        }
    if access_jwt_expired:
        scheme["content"]["application/json"]["examples"]["access_jwt_expired"] = {
            "summary": "JWT - Token de acceso expirado",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionError.ACCESS_JWT_EXPIRED.value,
                "data": {},
            },
        }
    if access_jwt_not_expired:
        scheme["content"]["application/json"]["examples"]["access_jwt_not_expired"] = {
            "summary": "JWT - Token de acceso no ha expirado",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionError.ACCESS_JWT_NOT_EXPIRED.value,
                "data": {},
            },
        }
    if refresh_jwt_invalid:
        scheme["content"]["application/json"]["examples"]["refresh_jwt_invalid"] = {
            "summary": "JWT - Token de actualización inválido",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionError.REFRESH_JWT_INVALID.value,
                "data": {},
            },
        }
    if refresh_jwt_expired:
        scheme["content"]["application/json"]["examples"]["refresh_jwt_expired"] = {
            "summary": "JWT - Token de actualización expirado",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionError.REFRESH_JWT_EXPIRED.value,
                "data": {},
            },
        }
    if jwt_user_not_found:
        scheme["content"]["application/json"]["examples"]["jwt_user_not_found"] = {
            "summary": "JWT - Usuario del token de acceso no existe",
            "value": {
                "success": False,
                "pagination": False,
                "message": AuthExceptionError.JWT_USER_NOT_FOUND.value,
                "data": {},
            },
        }

    return scheme


def response_scheme_404() -> dict[str, Any]:
    """Genera el esquema OpenAPI de error 404 (Not Found) cuando un recurso no existe."""

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
                    "message": CommonException.RESOURCE_NOT_FOUND.value,
                    "data": {},
                },
            }
        },
    }


def response_scheme_403() -> dict[str, Any]:
    """Genera el esquema OpenAPI de error 403 (Forbidden) por permisos insuficientes."""

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
                    "message": CommonException.PERMISSION_DENIED.value,
                    "data": {},
                },
            }
        },
    }


def response_scheme_409(
    product_has_reserved_stock: bool = False,
    category_has_dependencies: bool = False,
    order_already_has_payment: bool = False,
) -> dict[str, Any]:
    """Genera el esquema OpenAPI de error 409 (Conflict) por violaciones de reglas de dominio."""

    scheme: dict[str, Any] = {
        "description": "**(CONFLICT)** Conflicto con el estado actual del recurso.",
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

    if category_has_dependencies:
        scheme["content"]["application/json"]["examples"]["category_has_dependencies"] = {
            "summary": "Categoría con productos asociados",
            "value": {
                "success": False,
                "pagination": False,
                "message": InventoryException.CATEGORY_HAS_DEPENDENCIES.value,
                "data": {},
            },
        }
    if product_has_reserved_stock:
        scheme["content"]["application/json"]["examples"]["product_has_reserved_stock"] = {
            "summary": "Producto con stock reservado",
            "value": {
                "success": False,
                "pagination": False,
                "message": InventoryException.PRODUCT_HAS_RESERVED_STOCK.value,
                "data": {},
            },
        }
    if order_already_has_payment:
        scheme["content"]["application/json"]["examples"]["order_already_has_payment"] = {
            "summary": "Orden de compra con pago asociado",
            "value": {
                "success": False,
                "pagination": False,
                "message": PaymentException.ORDER_ALREADY_HAS_PAYMENT.value,
                "data": {},
            },
        }

    return scheme


def response_scheme_503(db_unavailable: bool = False) -> dict[str, Any]:
    """Genera el esquema OpenAPI de error 503 (Service Unavailable) para fallos del servicio."""

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
                "message": CommonException.DB_UNAVAILABLE.value,
                "data": {},
            },
        }

    return scheme


def response_scheme_502(
    payment_gateway_config_error: bool = False,
    payment_gateway_unavailable: bool = False,
    payment_gateway_rejected: bool = False,
    payment_gateway_invalid_response: bool = False,
    payment_email_delivery_error: bool = False,
) -> dict[str, Any]:
    """
    Genera el esquema OpenAPI de error 502 (Bad Gateway) para fallos devueltos por servicios
    externos intermediarios.
    """

    scheme: dict[str, Any] = {
        "description": "**(BAD_GATEWAY)** Error devuelto por un servicio externo intermediario.",
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

    if payment_gateway_config_error:
        scheme["content"]["application/json"]["examples"]["payment_gateway_config_error"] = {
            "summary": "Error de configuración del servicio de pago",
            "value": {
                "success": False,
                "pagination": False,
                "message": PaymentException.GATEWAY_CONFIG_ERROR.value,
                "data": {},
            },
        }
    if payment_gateway_unavailable:
        scheme["content"]["application/json"]["examples"]["payment_gateway_unavailable"] = {
            "summary": "Servicio de pago no disponible",
            "value": {
                "success": False,
                "pagination": False,
                "message": PaymentException.GATEWAY_UNAVAILABLE.value,
                "data": {},
            },
        }
    if payment_gateway_rejected:
        scheme["content"]["application/json"]["examples"]["payment_gateway_rejected"] = {
            "summary": "Petición rechazada por el servicio de pago",
            "value": {
                "success": False,
                "pagination": False,
                "message": PaymentException.GATEWAY_REJECTED.value,
                "data": {},
            },
        }
    if payment_gateway_invalid_response:
        scheme["content"]["application/json"]["examples"]["payment_gateway_invalid_response"] = {
            "summary": "Respuesta no válida del servicio de pago",
            "value": {
                "success": False,
                "pagination": False,
                "message": PaymentException.GATEWAY_INVALID_RESPONSE.value,
                "data": {},
            },
        }
    if payment_email_delivery_error:
        scheme["content"]["application/json"]["examples"]["payment_email_delivery_error"] = {
            "summary": "Fallo con el correo electrónico del cliente de la transacción",
            "value": {
                "success": False,
                "pagination": False,
                "message": PaymentException.DELIVERY_ERROR.value,
                "data": {},
            },
        }

    return scheme


def response_scheme_504(
    payment_gateway_timeout: bool = False,
    payment_gateway_connection_error: bool = False,
) -> dict[str, Any]:
    """Genera el esquema OpenAPI de error 504 (Gateway Timeout) para tiempos agotados o red."""

    scheme: dict[str, Any] = {
        "description": (
            "**(GATEWAY_TIMEOUT)** El tiempo de espera con un servicio externo intermediario "
            "se agotó o hubo un error de conectividad."
        ),
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

    if payment_gateway_timeout:
        scheme["content"]["application/json"]["examples"]["payment_gateway_timeout"] = {
            "summary": "Tiempo de respuesta del servicio de pago agotado",
            "value": {
                "success": False,
                "pagination": False,
                "message": PaymentException.GATEWAY_TIMEOUT.value,
                "data": {},
            },
        }
    if payment_gateway_connection_error:
        scheme["content"]["application/json"]["examples"]["payment_gateway_connection_error"] = {
            "summary": "Error de conexión con el servicio de pago",
            "value": {
                "success": False,
                "pagination": False,
                "message": PaymentException.GATEWAY_CONNECTION_ERROR.value,
                "data": {},
            },
        }

    return scheme


def response_scheme_500(
    smtp_credentials_not_configured: bool = False,
    smtp_authentication_error: bool = False,
) -> dict[str, Any]:
    """
    Genera el esquema OpenAPI de error 500 (Internal Server Error) para fallos de
    configuraciones internas del servidor.
    """

    scheme: dict[str, Any] = {
        "description": "**(INTERNAL_SERVER_ERROR)** Error en la configuración del servidor.",
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

    if smtp_credentials_not_configured:
        scheme["content"]["application/json"]["examples"]["smtp_credentials_not_configured"] = {
            "summary": "Credenciales de correo no configuradas",
            "value": {
                "success": False,
                "pagination": False,
                "message": EmailException.CREDENTIALS_NOT_CONFIGURED.value,
                "data": {},
            },
        }
    if smtp_authentication_error:
        scheme["content"]["application/json"]["examples"]["smtp_authentication_error"] = {
            "summary": "Error de autenticación con el servidor de correo",
            "value": {
                "success": False,
                "pagination": False,
                "message": EmailException.AUTHENTICATION_ERROR.value,
                "data": {},
            },
        }

    return scheme
