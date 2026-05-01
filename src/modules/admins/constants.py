from enum import Enum

ROLE = "admin"


class AdminEntity(Enum):
    """Enumeración que define constantes relacionadas con la entidad `Admin`."""

    # Descripciones para los campos de la entidad
    ID_DESCRIPTION = "Identificador único (UUID v4)."
    FIRST_NAMES_DESCRIPTION = "Primer y segundo nombre del administrador."
    LAST_NAMES_DESCRIPTION = "Primer y segundo apellido del administrador."
    DATE_JOINED_DESCRIPTION = "Fecha y hora de la creación del registro."
    ID_USER_DESCRIPTION = "ID asignado al administrador por el sistema."

    # Mensajes de error
    DOCUMENT_TYPE_INVALID = "El valor seleccionado no es válido."
    DOCUMENT_NUMBER_IN_USE = "Este número de documento ya está registrado."
    PHONE_IN_USE = "Este número de teléfono ya está registrado."

    # Propiedades para los campos de la entidad
    FIRST_NAMES_MAX_LENGTH = 40
    LAST_NAMES_MAX_LENGTH = 40
