from enum import Enum


class CustomerEntity(Enum):
    """Enumeración que define constantes relacionadas con la entidad `Customer`."""

    # Descripciones para los campos de la entidad
    ID_DESCRIPTION = "Identificador único (UUID v4)."
    FIRST_NAMES_DESCRIPTION = "Primer y segundo nombre del cliente."
    LAST_NAMES_DESCRIPTION = "Primer y segundo apellido del cliente."
    DOCUMENT_TYPE_DESCRIPTION = "Tipo de documento del cliente."
    DOCUMENT_NUMBER_DESCRIPTION = "Número del documento del cliente."
    PHONE_DESCRIPTION = "Número de teléfono del cliente."
    DATE_JOINED_DESCRIPTION = "Fecha y hora de la creación del registro."

    # Propiedades para los campos de la entidad
    FIRST_NAMES_MAX_LENGTH = 40
    LAST_NAMES_MAX_LENGTH = 40
    DOCUMENT_NUMBER_MAX_LENGTH = 13
    PHONE_MAX_LENGTH = 25


class DocumentTypesCustomer(Enum):
    """Enumeración que define los tipos de documentos para la entidad de un cliente."""

    RUT = "RUT"
    PASSPORT = "Pasaporte"
    IDENTIFICATION_NUMBER = "Cédula"
