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
    DATE_JOINED_DESCRIPTION = "Fecha y hora de la creación del registro."

    # Mensajes de error
    EMAIL_IN_USE = "Este correo electrónico ya está registrado."

    # Propiedades para los campos de la entidad
    EMAIL_MAX_LENGTH = 60
    PASSWORD_HASH_MAX_LENGTH = 128
    PASSWORD_MAX_LENGTH = 30
    PASSWORD_MIN_LENGTH = 8
    ROLE_MAX_LENGTH = 30


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
    TOKEN_DESCRIPTION = "JWT de autenticación."
    USER_ID_DESCRIPTION = "ID del usuario al que pertenece el token."
    EXPIRES_AT_DESCRIPTION = "Fecha y hora de expiración del token."
    ACCESS_TOKEN_DESCRIPTION = "Token de acceso JWT para autenticación de un usuario."
    DATE_JOINED_DESCRIPTION = "Fecha y hora de la creación del registro."

    # Propiedades para los campos de la entidad
    TOKEN_MAX_LENGTH = 512
