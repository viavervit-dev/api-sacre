from enum import Enum


class UserRoles(Enum):
    """Enumeración que define constantes relacionadas con los roles de usuario."""

    CUSTOMER = "customer"
    CUSTOMER_WHOLESALE = "customer_wholesale"
    ADMINISTRATOR = "admin"


class UserEntity(Enum):
    """Metadatos asociados a la entidad `User`."""

    # Descripciones para los campos de la entidad
    EMAIL_DESCRIPTION = "Correo electrónico del usuario."
    PASSWORD_HASH_DESCRIPTION = "Hash encriptado de la contraseña del usuario."
    PASSWORD_DESCRIPTION = "Contraseña del usuario"
    FIRST_NAME_DESCRIPTION = "Nombres del usuario."
    LAST_NAME_DESCRIPTION = "Apellidos del usuario."
    ROLE_NAME_DESCRIPTION = "Rol del usuario."
    ROLE_DATA_DESCRIPTION = "Datos específicos del rol del usuario."
    SESSION_VERSION_DESCRIPTION = "Control para la revocación global de tokens de acceso."

    # Mensajes de error
    EMAIL_IN_USE = "Este correo electrónico ya está registrado."

    # Propiedades para los campos de la entidad
    EMAIL_MAX_LENGTH = 60
    PASSWORD_HASH_MAX_LENGTH = 128
    PASSWORD_MAX_LENGTH = 30
    PASSWORD_MIN_LENGTH = 8
    ROLE_MAX_LENGTH = 30
    SESSION_VERSION_MIN_VALUE = 1


class PermissionEntity(Enum):
    """Metadatos asociados a la entidad `Permission`."""

    # Descripciones para los campos de la entidad
    NAME_DESCRIPTION = "Nombre del permiso."

    # Propiedades para los campos de la entidad
    NAME_MAX_LENGTH = 100


class GroupEntity(Enum):
    """Metadatos asociados a la entidad `Group`."""

    # Descripciones para los campos de la entidad
    NAME_DESCRIPTION = "Nombre del grupo."

    # Propiedades para los campos de la entidad
    NAME_MAX_LENGTH = 100


class ExceptionErrorMessages(Enum):
    """
    Enumeración que define constantes relacionadas con los mensajes de error para excepciones
    generales.
    """

    CREDENTIALS_INVALID = "Correo electrónico o contraseña incorrecta."
    ACCESS_JWT_MISSING = "No se encontró el token de acceso en la petición."
    REFRESH_JWT_MISSING = "No se encontró el token de actualización en la petición."
    ACCESS_JWT_EXPIRED = "El token de acceso ha expirado."
    ACCESS_JWT_NOT_EXPIRED = "El token de acceso no ha expirado."
    REFRESH_JWT_EXPIRED = "El token de actualización ha expirado."
    ACCESS_JWT_INVALID = "Token de acceso inválido."
    REFRESH_JWT_INVALID = "Token de actualización inválido."
    JWT_USER_NOT_FOUND = "El usuario asociado al token de acceso no existe."
    SESSION_CORRUPTED = "Sesión inválida o corrupta. Por favor, inicie sesión nuevamente."
    AUTH_SESSION_EXPIRED = "Las credenciales de autenticación son inválidas o han expirado."
