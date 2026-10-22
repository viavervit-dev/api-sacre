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


class OrderEntity(Enum):
    """Metadatos asociados a la entidad `Order`."""

    # Descripciones para los campos de la entidad
    STATUS_DESCRIPTION = "Estado actual de la orden."
    CUSTOMER_DATA_DESCRIPTION = "Datos del cliente que realiza la orden."
    PRODUCT_DATA_DESCRIPTION = "Datos de los productos incluidos en la orden."
    ORDER_NUMBER_DESCRIPTION = "Código de referencia creado por el cliente (navegador)."
    UNITS_DESCRIPTION = "Cantidad total de unidades de productos de la orden."
    SUBTOTAL_DESCRIPTION = "Valor neto de la orden."
    TOTAL_DESCRIPTION = "Valor total final de la orden."
    TAX_AMOUNT_DESCRIPTION = "Total de impuestos aplicados de la orden."
    UNITS_PRODUCT_DESCRIPTION = "Cantidad de unidades del producto de un tipo."
    SUBTOTAL_PRODUCT_DESCRIPTION = "Valor neto de los productos de un tipo."
    TOTAL_PRODUCT_DESCRIPTION = "Valor total final de los productos de un tipo."
    TAX_AMOUNT_PRODUCT_DESCRIPTION = "Total de impuestos aplicados a los productos de un tipo."
    PERCENTAGE_DESCRIPTION = "Porcentaje adicional para aplicar a un valor base."
    AMOUNT_DESCRIPTION = "Monto base al que se le va a agregar un porcentaje."

    # Mensajes de error
    ORDER_NUMBER_EXISTS = "Este número de orden ya está registrado."
    PRODUCT_NOT_FOUND = "El producto no existe."
    SUBTOTAL_INVALID = "El subtotal no coincide con la suma del subtotal de los productos."
    UNITS_INVALID = "Las unidades no coinciden con la suma de las unidades de los productos."
    TOTAL_INVALID = "El total de la orden no coincide con la suma del total de los productos."
    TOTAL_PRODUCT_INVALID = (
        "El total del producto no coincide con la suma del subtotal y el impuesto."
    )
    TAX_AMOUNT_INVALID = (
        "El monto de impuestos no coincide con la suma de los impuestos de los productos."
    )
    TAX_AMOUNT_PRODUCT_INVALID = (
        "El impuesto del producto no coincide con el cálculo aplicado a su subtotal."
    )

    # Propiedades para los campos de la entidad
    AMOUNT_MAX_DIGITS = 8
    AMOUNT_DECIMAL_PLACES = 2
    AMOUNT_MAX_VALUE = Decimal(value="999999.99")
    AMOUNT_MIN_VALUE = Decimal(value="0.00")
    PERCENTAGE_MAX_DIGITS = 5
    PERCENTAGE_DECIMAL_PLACES = 4
    PERCENTAGE_MAX_VALUE = Decimal(value="2.0000")
    PERCENTAGE_MIN_VALUE = Decimal(value="0.0000")
    PRODUCTS_MIN_LENGTH = 1
    PRODUCTS_MAX_LENGTH = 9999
    SUBTOTAL_MAX_DIGITS = 7
    SUBTOTAL_DECIMAL_PLACES = 2
    SUBTOTAL_MAX_VALUE = Decimal(value="99999.99")
    SUBTOTAL_MIN_VALUE = Decimal(value="0.00")
    TOTAL_MAX_DIGITS = 8
    TOTAL_DECIMAL_PLACES = 2
    TOTAL_MAX_VALUE = Decimal(value="999999.99")
    TOTAL_MIN_VALUE = Decimal(value="0.00")
    TAX_AMOUNT_MAX_DIGITS = 7
    TAX_AMOUNT_DECIMAL_PLACES = 2
    TAX_AMOUNT_MAX_VALUE = Decimal(value="99999.99")
    TAX_AMOUNT_MIN_VALUE = Decimal(value="0.00")
    UNITS_MAX_VALUE = 99999
    UNITS_MIN_VALUE = 0
    UNITS_PRODUCT_MAX_VALUE = 9999
    UNITS_PRODUCT_MIN_VALUE = 0
    SUBTOTAL_PRODUCT_MAX_DIGITS = 7
    SUBTOTAL_PRODUCT_DECIMAL_PLACES = 2
    SUBTOTAL_PRODUCT_MAX_VALUE = Decimal(value="99999.99")
    SUBTOTAL_PRODUCT_MIN_VALUE = Decimal(value="0.00")
    TOTAL_PRODUCT_MAX_DIGITS = 8
    TOTAL_PRODUCT_DECIMAL_PLACES = 2
    TOTAL_PRODUCT_MAX_VALUE = Decimal(value="999999.99")
    TOTAL_PRODUCT_MIN_VALUE = Decimal(value="0.00")


class DecimalNumberEntity(Enum):
    """Metadatos y restricciones para operaciones con números decimales."""

    # Descripciones para los campos de la entidad
    DESCRIPTION = "Valor numérico decimal."
    LIST_DESCRIPTION = "Lista de valores numéricos decimales."

    # Propiedades
    MIN_LENGTH = 1
    MAX_LENGTH = 999
    MAX_DIGITS = 8
    DECIMAL_PLACES = 2
    MAX_VALUE = Decimal(value="999999.99")
    MIN_VALUE = Decimal(value="-999999.99")
