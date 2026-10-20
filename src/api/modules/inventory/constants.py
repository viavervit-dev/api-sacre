from decimal import Decimal
from enum import Enum


class CategoryEntity(Enum):
    """Metadatos asociados a la entidad `Category`."""

    # Descripciones para los campos de la entidad
    NAME_DESCRIPTION = "Nombre de la categoria."
    DESCRIPTION_DESCRIPTION = "Descripción de la categoria."
    STATUS_DESCRIPTION = "Estado de la categoria."

    # Mensajes de error
    NAME_IN_USE = "Este nombre ya está registrado."

    # Propiedades para los campos de la entidad
    NAME_MAX_LENGTH = 50
    DESCRIPTION_MAX_LENGTH = 1000


class ProductEntity(Enum):
    """Metadatos asociados a la entidad `Product`."""

    # Descripciones para los campos de la entidad
    NAME_DESCRIPTION = "Nombre del producto."
    CATEGORIES_DESCRIPTION = "Lista de categorías a las que pertenece el producto."
    DESCRIPTION_SHORT_DESCRIPTION = "Descripción corta del producto."
    DESCRIPTION_LONG_DESCRIPTION = "Descripción larga del producto."
    IMAGES_DESCRIPTION = "Lista de URLs de imágenes del producto."
    PRICE_NETO_DESCRIPTION = "Precio neto del producto."
    PRICE_SALE_DESCRIPTION = "Precio de venta del producto."
    PROFIT_MARGIN_DESCRIPTION = "Margen de ganancia aplicado al producto."
    TAX_AMOUNT_DESCRIPTION = "Total de impuestos aplicados."
    STOCK_TOTAL_DESCRIPTION = "Cantidad total de unidades existentes."
    STOCK_HAND_DESCRIPTION = "Unidades reservadas temporalmente en carritos de compra activos."
    STOCK_SALE_DESCRIPTION = "Unidades disponibles para la venta."
    STATUS_DESCRIPTION = "Estado del producto."
    EXCLUSIVE_DESCRIPTION = "Determina si el producto pertenece al catálogo público de productos.."
    WHOLESALER_ID_DESCRIPTION = "ID del cliente mayorista al que se le vende el producto."

    # Mensajes de error
    NAME_IN_USE = "Este nombre ya está registrado."
    URL_INVALID = "La URL proporcionada no es válida."
    CATEGORY_NOT_FOUND = "Esta categoría no existe."
    STOCK_TOTAL_INVALID = "El stock total no puede ser menor al stock en reserva."
    WHOLESALER_NOT_FOUND = "El cliente mayorista no existe."

    # Propiedades para los campos de la entidad
    NAME_MAX_LENGTH = 60
    DESCRIPTION_SHORT_MAX_LENGTH = 100
    DESCRIPTION_LONG_MAX_LENGTH = 1000
    MAXIMUM_NUMBER_IMAGES = 10
    MINIMUM_NUMBER_IMAGES = 3
    URL_IMAGES_MAX_LENGTH = 2048
    PRICE_NETO_MAX_DIGITS = 7
    PRICE_NETO_DECIMAL_PLACES = 2
    PRICE_NETO_MAX_VALUE = Decimal(value="99999.99")
    PRICE_NETO_MIN_VALUE = Decimal(value="0.00")
    PRICE_SALE_MAX_DIGITS = 7
    PRICE_SALE_DECIMAL_PLACES = 2
    PRICE_SALE_MAX_VALUE = Decimal(value="99999.99")
    PRICE_SALE_MIN_VALUE = Decimal(value="0.00")
    PROFIT_MARGIN_MAX_DIGITS = 5
    PROFIT_MARGIN_DECIMAL_PLACES = 4
    PROFIT_MARGIN_MAX_VALUE = Decimal(value="2.0000")
    PROFIT_MARGIN_MIN_VALUE = Decimal(value="0.0000")
    TAX_AMOUNT_MAX_DIGITS = 7
    TAX_AMOUNT_DECIMAL_PLACES = 2
    TAX_AMOUNT_MAX_VALUE = Decimal(value="99999.99")
    TAX_AMOUNT_MIN_VALUE = Decimal(value="0.00")
    STOCK_TOTAL_MAX_VALUE = 10000
    STOCK_TOTAL_MIN_VALUE = 0
    STOCK_HAND_MAX_VALUE = 10000
    STOCK_HAND_MIN_VALUE = 0
    STOCK_SALE_MAX_VALUE = 10000
    STOCK_SALE_MIN_VALUE = 0


class ExceptionErrorMessages(Enum):
    """
    Enumeración que define constantes relacionadas con los mensajes de error para excepciones
    generales.
    """

    CATEGORY_HAS_DEPENDENCIES = (
        "No se puede eliminar la categoría porque tiene productos asociados."
    )
    PRODUCT_HAS_RESERVED_STOCK = (
        "No se puede eliminar el producto porque actualmente tiene stock reservado."
    )
