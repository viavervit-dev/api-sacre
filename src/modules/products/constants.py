from enum import Enum


class CategoryEntity(Enum):
    """Enumeración que define constantes relacionadas con la entidad `Customer`."""

    # Descripciones para los campos de la entidad
    ID_DESCRIPTION = "Identificador único (UUID v4)."
    NAME_DESCRIPTION = "Nombre de la categoria."
    DESCRIPTION_DESCRIPTION = "Descripción de la categoria."
    PRODUCT_NUMBER_DESCRIPTION = "Número de productos de la categoria."
    STATUS_DESCRIPTION = "Estado de la categoria."
    DATE_JOINED_DESCRIPTION = "Fecha y hora de la creación del registro."

    # Mensajes de error
    NAME_IN_USE = "Este nombre ya está registrado."

    # Propiedades para los campos de la entidad
    NAME_MAX_LENGTH = 50
    DESCRIPTION_MAX_LENGTH = 1000
    MAXIMUM_NUMBER_PRODUCTS = 1000
    MINIMUM_NUMBER_PRODUCTS = 0
