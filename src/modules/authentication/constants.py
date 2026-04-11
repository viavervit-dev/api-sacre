from enum import Enum


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


class UserEntity(Enum):
    """Enumeración que define constantes relacionadas con la entidad `Users`."""

    # Descripciones para los campos de la entidad
    ID_DESCRIPTION = "Identificador único (UUID v4)."
    EMAIL_DESCRIPTION = "Correo electrónico del usuario."
    PASSWORD_HASH_DESCRIPTION = "Hash encriptado de la contraseña del usuario."
    DATE_JOINED_DESCRIPTION = "Fecha y hora de la creación del registro."

    # Propiedades para los campos de la entidad
    EMAIL_MAX_LENGTH = 60
    PASSWORD_HASH_MAX_LENGTH = 128
    PASSWORD_MAX_LENGTH = 30
    PASSWORD_MIN_LENGTH = 8
