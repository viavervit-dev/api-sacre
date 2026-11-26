from dataclasses import dataclass
from enum import StrEnum
from typing import Final


@dataclass(frozen=True, slots=True)
class CustomerConstants:
    """Reglas de dominio, límites técnicos y catálogo de errores para la entidad `Customer`."""

    class Limits:
        """Límites cuantitativos y restricciones técnicas para la entidad `Customer`."""

        FIRST_NAMES_MAX_LENGTH: int = 40
        LAST_NAMES_MAX_LENGTH: int = 40
        DOCUMENT_NUMBER_MAX_LENGTH: int = 13
        DOCUMENT_TYPE_MAX_LENGTH: int = 9
        PHONE_MAX_LENGTH: int = 25

    class Docs:
        """Descripciones y metadatos de documentación OpenAPI para la entidad `Customer`."""

        FIRST_NAMES_DESCRIPTION: str = "Primer y segundo nombre del cliente."
        LAST_NAMES_DESCRIPTION: str = "Primer y segundo apellido del cliente."
        DOCUMENT_TYPE_DESCRIPTION: str = "Tipo de documento del cliente."
        DOCUMENT_NUMBER_DESCRIPTION: str = "Número del documento del cliente."
        PHONE_DESCRIPTION: str = "Número de teléfono del cliente."

    class Errors:
        """Catálogo de mensajes de error estandarizados para la entidad `Customer`."""

        DOCUMENT_TYPE_INVALID: str = "El valor seleccionado no es válido."
        DOCUMENT_NUMBER_IN_USE: str = "Este número de documento ya está registrado."
        PHONE_IN_USE: str = "Este número de teléfono ya está registrado."


CUSTOMER_CONSTANTS: Final[CustomerConstants] = CustomerConstants()


class DocumentTypesCustomer(StrEnum):
    """Tipos de documentos de identificación admitidos para un cliente."""

    RUC = "RUC"
    PASSPORT = "Pasaporte"
    IDENTIFICATION_NUMBER = "Cédula"

    @classmethod
    def values(cls) -> list[str]:
        """Devuelve una lista de los valores de la enumeración."""

        return [item.value for item in cls]
