from enum import Enum

ROLE = "customer"


class ValidationErrorMessages(Enum):
    """Enumeración que define constantes relacionadas con los mensajes de error de validación.

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

    # Correo electrónico (EmailStr via email-validator)
    VALUE_ERROR_EMAIL = "El correo electrónico no tiene un formato válido."

    # Números enteros
    INT_TYPE = "El campo debe ser un número entero."
    INT_PARSING = "El valor ingresado no puede convertirse a número entero."

    # Números decimales
    FLOAT_TYPE = "El campo debe ser un número."
    FLOAT_PARSING = "El valor ingresado no puede convertirse a número."

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
