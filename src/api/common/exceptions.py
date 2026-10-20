from enum import Enum
from typing import Any


class DTOValidationErrorMessages(Enum):
    """
    Enumeración que define constantes relacionadas con los mensajes de error de validación.

    Los tipos de error corresponden a los códigos de error de Pydantic v2.
    Referencia: https://docs.pydantic.dev/latest/errors/validation_errors/
    """

    # Campos requeridos
    MISSING = "Este campo es obligatorio."
    EXTRA_FORBIDDEN = "Este campo no está permitido."

    # Texto
    STRING_TYPE = "El campo debe contener texto."
    STRING_TOO_LONG = "El texto ingresado supera el límite máximo de caracteres."
    STRING_TOO_SHORT = "El texto ingresado no alcanza el mínimo de caracteres requeridos."
    STRING_PATTERN_MISMATCH = "El formato del texto no es válido."
    STRING_UNICODE = "El texto contiene caracteres no válidos."

    # Correo electrónico
    VALUE_ERROR_EMAIL = "El correo electrónico no tiene un formato válido."

    # Números enteros
    INT_TYPE = "El campo debe ser un número entero."
    INT_PARSING = "El valor ingresado no puede convertirse a número entero."

    # Números decimales
    FLOAT_TYPE = "El campo debe ser un número."
    FLOAT_PARSING = "El valor ingresado no puede convertirse a número."
    DECIMAL_MAX_PLACES = "EL valor no puede tener más decimales."
    DECIMAL_MAX_DIGITS = "El valor no puede tener más dígitos."

    # Booleanos
    BOOL_TYPE = "El campo debe ser verdadero o falso."
    BOOL_PARSING = "El valor ingresado no puede interpretarse como verdadero o falso."

    # Restricciones numéricas
    GREATER_THAN = "El valor debe ser mayor al mínimo permitido."
    GREATER_THAN_EQUAL = "El valor debe ser mayor o igual al mínimo permitido."
    LESS_THAN = "El valor debe ser menor al máximo permitido."
    LESS_THAN_EQUAL = "El valor debe ser menor o igual al máximo permitido."
    MULTIPLE_OF = "El valor debe ser múltiplo del valor configurado."
    FINITE_NUMBER = "El valor debe ser un número finito."

    # Enumeraciones
    ENUM = "El valor seleccionado no es válido."
    LITERAL_ERROR = "El valor no corresponde a ninguna de las opciones válidas."

    # UUID
    UUID_TYPE = "El identificador debe ser un UUID válido."
    UUID_PARSING = "El identificador no tiene un formato UUID válido."
    UUID_VERSION = "La versión del UUID no es la requerida."

    # JSON
    JSON_INVALID = "El cuerpo de la solicitud contiene JSON inválido."
    JSON_TYPE = "Se esperaba un objeto JSON."

    # Genérico
    VALUE_ERROR = "El valor ingresado no es válido."


class ExceptionErrorMessages(Enum):
    """
    Enumeración que define constantes relacionadas con los mensajes de error para excepciones
    generales.
    """

    DB_UNAVAILABLE = "El servicio de base de datos no está disponible."
    REQUEST_DATA_INVALID = "Los datos enviados en la petición no son válidos."
    RESOURCE_NOT_FOUND = "El recurso no existe en la base de datos."
    USER_NOT_FOUND = "El usuario no existe en la base de datos."
    PERMISSION_DENIED = "El usuario no tiene los permisos necesarios."


class BaseAppException(Exception):
    """Clase base para manejar datos dinámicos en las excepciones de la app."""

    default_message = "Ha ocurrido un error inesperado en la aplicación."

    def __init__(self, message: str | None = None, data: dict[str, Any] = {}) -> None:  # noqa
        self.message = message or self.default_message
        self.data = data
        super().__init__(self.message)


class AuthenticationFailed(BaseAppException):
    """Cuando no se logra autenticar un usuario."""

    pass


class ResourceNotFound(BaseAppException):
    """El recurso solicitado en la petición no existe."""

    default_message = ExceptionErrorMessages.RESOURCE_NOT_FOUND.value


class UserNotFound(BaseAppException):
    """Cuando un usuario no existe."""

    default_message = ExceptionErrorMessages.USER_NOT_FOUND.value


class MissingJWT(BaseAppException):
    """Cuando no se encuentran las cookies de JWT en la petición."""

    pass


class InvalidJWT(BaseAppException):
    """Cuando se proporciona un token JWT inválido."""

    pass


class PermissionDenied(BaseAppException):
    """Cuando un usuario autenticado no tiene los permisos necesarios."""

    default_message = ExceptionErrorMessages.PERMISSION_DENIED.value


class DomainRuleViolation(BaseAppException):
    """Cuando se viola una regla de dominio."""

    pass
