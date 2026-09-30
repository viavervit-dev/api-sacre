from enum import Enum, StrEnum


class CustomerEntity(Enum):
    """Constantes y metadatos asociados a la entidad `Customer`."""

    # Descripciones para los campos de la entidad
    FIRST_NAMES_DESCRIPTION = "Primer y segundo nombre del cliente."
    LAST_NAMES_DESCRIPTION = "Primer y segundo apellido del cliente."
    DOCUMENT_TYPE_DESCRIPTION = "Tipo de documento del cliente."
    DOCUMENT_NUMBER_DESCRIPTION = "Número del documento del cliente."
    PHONE_DESCRIPTION = "Número de teléfono del cliente."
    ID_USER_DESCRIPTION = "ID asignado al cliente por el sistema."

    # Mensajes de error
    DOCUMENT_TYPE_INVALID = "El valor seleccionado no es válido."
    DOCUMENT_NUMBER_IN_USE = "Este número de documento ya está registrado."
    PHONE_IN_USE = "Este número de teléfono ya está registrado."

    # Propiedades para los campos de la entidad
    FIRST_NAMES_MAX_LENGTH = 40
    LAST_NAMES_MAX_LENGTH = 40
    DOCUMENT_NUMBER_MAX_LENGTH = 13
    DOCUMENT_TYPE_MAX_LENGTH = 9
    PHONE_MAX_LENGTH = 25


class DocumentTypesCustomer(StrEnum):
    """Tipos de documentos de identificación admitidos para un cliente."""

    RUC = "RUC"
    PASSPORT = "Pasaporte"
    IDENTIFICATION_NUMBER = "Cédula"

    @classmethod
    def values(cls) -> list[str]:
        """Devuelve una lista de los valores de la enumeración."""

        return [item.value for item in cls]


class AdminEntity(Enum):
    """Constantes y metadatos asociados a la entidad `Admin`."""

    # Descripciones para los campos de la entidad
    FIRST_NAMES_DESCRIPTION = "Primer y segundo nombre del administrador."
    LAST_NAMES_DESCRIPTION = "Primer y segundo apellido del administrador."
    ID_USER_DESCRIPTION = "ID asignado al administrador por el sistema."

    # Propiedades para los campos de la entidad
    FIRST_NAMES_MAX_LENGTH = 40
    LAST_NAMES_MAX_LENGTH = 40


class WholesaleEntity(Enum):
    """Constantes y metadatos asociados a la entidad `Wholesale`."""

    # Descripciones para los campos de la entidad
    NAME_OR_COMPANY_NAME_DESCRIPTION = "Nombre o razón social del mayorista."
    EMAIL_DESCRIPTION = "Correo electrónico del mayorista."
    RUC_DESCRIPTION = "Registro Único de Contribuyentes del mayorista."
    PHONE_DESCRIPTION = "Número de teléfono del mayorista."
    LOCATION_DESCRIPTION = "Datos de ubicación y dirección de entrega."
    EXTRA_CONTACTS_DESCRIPTION = "Contactos adicionales del mayorista."
    NAME_CONTACT_DESCRIPTION = "Nombre del contacto adicional."
    POSITION_CONTACT_DESCRIPTION = "Cargo del contacto adicional."

    # Mensajes de error
    NAME_OR_COMPANY_NAME_IN_USE = "Nombre o razón social ya esta registrado."
    PHONE_IN_USE = "Este número de teléfono ya está registrado."
    RUC_IN_USE = "Nombre o razón social ya esta registrado."

    # Propiedades para los campos de la entidad
    NAME_OR_COMPANY_NAME_MAX_LENGTH = 100
    NAME_CONTACT_MAX_LENGTH = 100
    POSITION_CONTACT_MAX_LENGTH = 100
    EMAIL_MAX_LENGTH = 60
    RUC_MAX_LENGTH = 13
    PHONE_MAX_LENGTH = 25


class Ecuador(StrEnum):
    """Enumeración del país Ecuador para normalización de direcciones."""

    ECUADOR = "Ecuador"

    @classmethod
    def values(cls) -> list[str]:
        """Devuelve una lista de los valores de la enumeración."""

        return [item.value for item in cls]
