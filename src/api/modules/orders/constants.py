from decimal import Decimal
from enum import Enum, StrEnum


class OrderStatus(StrEnum):
    """Estados posibles de un pedido."""

    PENDING_PAYMENT = "Pendiente de pago"
    PAID = "Pago confirmado"
    CANCELLED = "Cancelado"
    FAILED = "Fallido"

    @classmethod
    def values(cls) -> list[str]:
        """Devuelve una lista de los valores de la enumeración."""

        return [item.value for item in cls]


class Currency(StrEnum):
    """Tipos de moneda admitidos para un pedido."""

    USD = "USD"

    @classmethod
    def values(cls) -> list[str]:
        """Devuelve una lista de los valores de la enumeración."""

        return [item.value for item in cls]


class OrderEntity(Enum):
    """Metadatos asociados a la entidad `Order`."""

    # Descripciones para los campos de la entidad
    STATUS_DESCRIPTION = "Estado actual del pedido."
    CUSTOMER_DATA_DESCRIPTION = "Datos del cliente que realiza la compra."
    PRODUCT_DATA_DESCRIPTION = "Datos de los productos incluidos en el pedido."
    ORDER_NUMBER_DESCRIPTION = "Código de referencia."
    CURRENCY_DESCRIPTION = "Código ISO de la moneda."
    SUBTOTAL_DESCRIPTION = "Valor neto de todos los productos, sin cargo de impuestos ni envío."
    TAX_AMOUNT_DESCRIPTION = "Total de impuestos / IVA aplicados."
    SHIPING_COST_DESCRIPTION = "Costo de envío del pedido."
    DISCOUNT_AMOUNT_DESCRIPTION = "Monto de descuento aplicado."
    DISCOUNT_PERCENTAGE_DESCRIPTION = "Porcentaje de descuento aplicado."
    TOTAL_AMOUNT_DESCRIPTION = "Monto total final a pagar."

    # Propiedades para los campos de la entidad
    SUBTOTAL_MAX_DIGITS = 8
    SUBTOTAL_DECIMAL_PLACES = 2
    SUBTOTAL_MAX_VALUE = Decimal(value="999999.99")
    SUBTOTAL_MIN_VALUE = Decimal(value="0.00")
    TAX_AMOUNT_MAX_DIGITS = 7
    TAX_AMOUNT_DECIMAL_PLACES = 2
    TAX_AMOUNT_MAX_VALUE = Decimal(value="99999.99")
    TAX_AMOUNT_MIN_VALUE = Decimal(value="0.00")
    SHIPING_COST_MAX_DIGITS = 7
    SHIPING_COST_DECIMAL_PLACES = 2
    SHIPING_COST_MAX_VALUE = Decimal(value="99999.99")
    SHIPING_COST_MIN_VALUE = Decimal(value="0.00")
    DISCOUNT_AMOUNT_MAX_DIGITS = 7
    DISCOUNT_AMOUNT_DECIMAL_PLACES = 2
    DISCOUNT_AMOUNT_MAX_VALUE = Decimal(value="99999.99")
    DISCOUNT_AMOUNT_MIN_VALUE = Decimal(value="0.00")
    DISCOUNT_PERCENTAGE_MAX_DIGITS = 5
    DISCOUNT_PERCENTAGE_DECIMAL_PLACES = 4
    DISCOUNT_PERCENTAGE_MAX_VALUE = Decimal(value="1.0000")
    DISCOUNT_PERCENTAGE_MIN_VALUE = Decimal(value="0.0000")
    TOTAL_AMOUNT_MAX_DIGITS = 8
    TOTAL_AMOUNT_DECIMAL_PLACES = 2
    TOTAL_AMOUNT_MAX_VALUE = Decimal(value="999999.99")
    TOTAL_AMOUNT_MIN_VALUE = Decimal(value="0.00")
