from enum import Enum


class UserRoles(Enum):
    """Enumeración que define constantes relacionadas con los roles de usuario."""

    CUSTOMER = "customer"
    ADMINISTRATOR = "admin"


class UserEntity(Enum):
    """Enumeración que define constantes relacionadas con la entidad `Users`."""

    # Descripciones para los campos de la entidad
    ID_DESCRIPTION = "Identificador único (UUID v4)."
    EMAIL_DESCRIPTION = "Correo electrónico del usuario."
    PASSWORD_HASH_DESCRIPTION = "Hash encriptado de la contraseña del usuario."
    PASSWORD_DESCRIPTION = "Contraseña del usuario"
    FIRST_NAME_DESCRIPTION = "Nombres del usuario."
    LAST_NAME_DESCRIPTION = "Apellidos del usuario."
    ROLE_NAME_DESCRIPTION = "Rol del usuario."
    ROLE_DATA_DESCRIPTION = "Datos específicos del rol del usuario."
    SESSION_VERSION_DESCRIPTION = "Control para la revocación global de tokens de acceso."
    DATE_JOINED_DESCRIPTION = "Fecha y hora de la creación del registro."

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
    """Enumeración que define constantes relacionadas con la entidad `Permissions`."""

    # Descripciones para los campos de la entidad
    ID_DESCRIPTION = "Identificador único (UUID v4)."
    NAME_DESCRIPTION = "Nombre del permiso."
    DATE_JOINED_DESCRIPTION = "Fecha y hora de la creación del registro."

    # Propiedades para los campos de la entidad
    NAME_MAX_LENGTH = 100


class GroupEntity(Enum):
    """Enumeración que define constantes relacionadas con la entidad `Groups`."""

    # Descripciones para los campos de la entidad
    ID_DESCRIPTION = "Identificador único (UUID v4)."
    NAME_DESCRIPTION = "Nombre del grupo."
    DATE_JOINED_DESCRIPTION = "Fecha y hora de la creación del registro."

    # Propiedades para los campos de la entidad
    NAME_MAX_LENGTH = 100


class JWTEntity(Enum):
    """Enumeración que define constantes relacionadas con la entidad `JWT`."""

    # Descripciones para los campos de la entidad
    ID_DESCRIPTION = "Identificador único (UUID v4)."
    TOKEN_DESCRIPTION = "JWT almacenado en la lista negra para revocación de tokens."
    JTI_DESCRIPTION = "Identificador único del token."
    TOKEN_TYPE_DESCRIPTION = "Tipo de token."
    USER_ID_DESCRIPTION = "ID del usuario al que pertenece el token."
    ACCESS_TOKEN_DESCRIPTION = "Token de acceso JWT para autenticación de un usuario."
    DATE_JOINED_DESCRIPTION = "Fecha y hora de la creación del registro."

    # Propiedades para los campos de la entidad
    TOKEN_TYPE_MAX_LENGTH = 20
    TOKEN_MAX_LENGTH = 512
    JTI_MAX_LENGTH = 200


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
    PERMISSION_DENIED = "El usuario no tiene los permisos necesarios."
    SESSION_CORRUPTED = "Sesión inválida o corrupta. Por favor, inicie sesión nuevamente."
    AUTH_SESSION_EXPIRED = "Las credenciales de autenticación son inválidas o han expirado."
