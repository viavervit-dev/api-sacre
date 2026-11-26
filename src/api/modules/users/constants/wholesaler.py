from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True, slots=True)
class WholesalerConstants:
    """Reglas de dominio, límites técnicos y catálogo de errores para la entidad `Wholesaler`."""

    class Limits:
        """Límites cuantitativos y restricciones técnicas para la entidad `Wholesaler`."""

        NAME_OR_COMPANY_NAME_MAX_LENGTH: int = 100
        NAME_CONTACT_MAX_LENGTH: int = 100
        POSITION_CONTACT_MAX_LENGTH: int = 100
        EMAIL_MAX_LENGTH: int = 60
        RUC_MAX_LENGTH: int = 13
        PHONE_MAX_LENGTH: int = 25

    class Docs:
        """Descripciones y metadatos de documentación OpenAPI para la entidad `Wholesaler`."""

        NAME_OR_COMPANY_NAME_DESCRIPTION: str = "Nombre o razón social del cliente mayorista."
        PRODUCTS_DESCRIPTION: str = "Lista de productos del cliente mayorista."
        EMAIL_DESCRIPTION: str = "Correo electrónico del cliente mayorista."
        RUC_DESCRIPTION: str = "Registro Único de Contribuyentes del cliente mayorista."
        PHONE_DESCRIPTION: str = "Número de teléfono del cliente mayorista."
        LOCATION_DESCRIPTION: str = "Datos de ubicación y dirección de entrega."
        EXTRA_CONTACTS_DESCRIPTION: str = "Contactos adicionales del cliente mayorista."
        NAME_CONTACT_DESCRIPTION: str = "Nombre del contacto adicional."
        POSITION_CONTACT_DESCRIPTION: str = "Cargo del contacto adicional."

    class Errors:
        """Catálogo de mensajes de error estandarizados para la entidad `Wholesaler`."""

        NAME_OR_COMPANY_NAME_IN_USE: str = "Nombre o razón social ya esta registrado."
        PHONE_IN_USE: str = "Este número de teléfono ya está registrado."
        RUC_IN_USE: str = "Nombre o razón social ya esta registrado."


WHOLESALER_CONSTANTS: Final[WholesalerConstants] = WholesalerConstants()
