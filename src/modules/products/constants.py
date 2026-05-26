from decimal import Decimal
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


class ProductEntity(Enum):
    """Enumeración que define constantes relacionadas con la entidad `Product`."""

    # Descripciones para los campos de la entidad
    ID_DESCRIPTION = "Identificador único (UUID v4)."
    NAME_DESCRIPTION = "Nombre del producto."
    CATEGORIES_DESCRIPTION = "Lista de categorías a las que pertenece el producto."
    DESCRIPTION_SHORT_DESCRIPTION = "Descripción corta del producto."
    DESCRIPTION_LONG_DESCRIPTION = "Descripción larga del producto."
    IMAGES_DESCRIPTION = "Lista de URLs de imágenes del producto."
    PRICE_NETO_DESCRIPTION = "Precio NETO del producto, sin impuestos."
    PRICE_SALE_DESCRIPTION = "Precio de venta del producto, con impuestos."
    IVA_DESCRIPTION = "Impuesto al valor agregado aplicado al producto."
    STOCK_TOTAL_DESCRIPTION = "Cantidad total de unidades existentes."
    STOCK_HAND_DESCRIPTION = "Unidades reservadas temporalmente en carritos de compra activos."
    STOCK_SALE_DESCRIPTION = "Unidades disponibles para la venta."
    STATUS_DESCRIPTION = "Estado del producto."
    DATE_JOINED_DESCRIPTION = "Fecha y hora de la creación del registro."

    # Mensajes de error
    NAME_IN_USE = "Este nombre ya está registrado."
    URL_INVALID = "La URL proporcionada no es válida."
    CATEGORY_NOT_FOUND = "Esta categoría no existe."

    # Propiedades para los campos de la entidad
    NAME_MAX_LENGTH = 60
    DESCRIPTION_SHORT_MAX_LENGTH = 100
    DESCRIPTION_LONG_MAX_LENGTH = 1000
    MAXIMUM_NUMBER_IMAGES = 10
    MINIMUM_NUMBER_IMAGES = 3
    URL_IMAGES_MAX_LENGTH = 2048
    PRICE_NETO_MAX_DIGITS = 7
    PRICE_NETO_DECIMAL_PLACES = 2
    PRICE_NETO_MAX_VALUE = Decimal(value="10000.00")
    PRICE_NETO_MIN_VALUE = Decimal(value="0.00")
    PRICE_SALE_MAX_DIGITS = 7
    PRICE_SALE_DECIMAL_PLACES = 2
    PRICE_SALE_MAX_VALUE = Decimal(value="10000.00")
    PRICE_SALE_MIN_VALUE = Decimal(value="0.00")
    IVA_MAX_DIGITS = 5
    IVA_DECIMAL_PLACES = 4
    IVA_MAX_VALUE = Decimal(value="1.0000")
    IVA_MIN_VALUE = Decimal(value="0.0000")
    STOCK_TOTAL_MAX_VALUE = 10000
    STOCK_TOTAL_MIN_VALUE = 0
    STOCK_HAND_MAX_VALUE = 10000
    STOCK_HAND_MIN_VALUE = 0
    STOCK_SALE_MAX_VALUE = 10000
    STOCK_SALE_MIN_VALUE = 0
