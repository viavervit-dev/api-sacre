from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from typing import Final


class OrderStatus(StrEnum):
    """Estados posibles de una orden de compra."""

    PENDING_PAYMENT = "Pendiente de pago"
    PAID = "Pago confirmado"
    CANCELLED = "Cancelado"

    @classmethod
    def values(cls) -> list[str]:
        """Devuelve una lista de los valores de la enumeración."""

        return [item.value for item in cls]


class OrderDescription(StrEnum):
    """Descripciones predefinidas para el propósito de una orden/transacción."""

    PURCHASE_ORDER = "Orden de compra"
    DONATION = "Donación"
    PAYMENT_LINK = "Link de pago"
    PAYMENT_GATEWAY = "Pasarela de pago"

    @classmethod
    def values(cls) -> list[str]:
        """Devuelve una lista de los valores de la enumeración."""

        return [item.value for item in cls]


@dataclass(frozen=True, slots=True)
class OrderConstants:
    """Reglas de dominio, límites técnicos y catálogo de errores para la entidad `Order`."""

    class Limits:
        """Límites cuantitativos y restricciones técnicas para la entidad `Order`."""

        AMOUNT_MAX_DIGITS: int = 8
        AMOUNT_DECIMAL_PLACES: int = 2
        AMOUNT_MAX_VALUE: Decimal = Decimal(value="999999.99")
        AMOUNT_MIN_VALUE: Decimal = Decimal(value="0.00")
        PERCENTAGE_MAX_DIGITS: int = 5
        PERCENTAGE_DECIMAL_PLACES: int = 4
        PERCENTAGE_MAX_VALUE: Decimal = Decimal(value="2.0000")
        PERCENTAGE_MIN_VALUE: Decimal = Decimal(value="0.0000")
        PRODUCTS_MIN_LENGTH: int = 1
        PRODUCTS_MAX_LENGTH: int = 9999
        SUBTOTAL_MAX_DIGITS: int = 7
        SUBTOTAL_DECIMAL_PLACES: int = 2
        SUBTOTAL_MAX_VALUE: Decimal = Decimal(value="99999.99")
        SUBTOTAL_MIN_VALUE: Decimal = Decimal(value="0.00")
        TOTAL_MAX_DIGITS: int = 8
        TOTAL_DECIMAL_PLACES: int = 2
        TOTAL_MAX_VALUE: Decimal = Decimal(value="999999.99")
        TOTAL_MIN_VALUE: Decimal = Decimal(value="0.00")
        TAX_AMOUNT_MAX_DIGITS: int = 7
        TAX_AMOUNT_DECIMAL_PLACES: int = 2
        TAX_AMOUNT_MAX_VALUE: Decimal = Decimal(value="99999.99")
        TAX_AMOUNT_MIN_VALUE: Decimal = Decimal(value="0.00")
        UNITS_MAX_VALUE: int = 99999
        UNITS_MIN_VALUE: int = 0
        UNITS_PRODUCT_MAX_VALUE: int = 9999
        UNITS_PRODUCT_MIN_VALUE: int = 0
        SUBTOTAL_PRODUCT_MAX_DIGITS: int = 7
        SUBTOTAL_PRODUCT_DECIMAL_PLACES: int = 2
        SUBTOTAL_PRODUCT_MAX_VALUE: Decimal = Decimal(value="99999.99")
        SUBTOTAL_PRODUCT_MIN_VALUE: Decimal = Decimal(value="0.00")
        TOTAL_PRODUCT_MAX_DIGITS: int = 8
        TOTAL_PRODUCT_DECIMAL_PLACES: int = 2
        TOTAL_PRODUCT_MAX_VALUE: Decimal = Decimal(value="999999.99")
        TOTAL_PRODUCT_MIN_VALUE: Decimal = Decimal(value="0.00")

    class Docs:
        """Descripciones y metadatos de documentación OpenAPI para la entidad `Order`."""

        STATUS_DESCRIPTION: str = "Estado actual de la orden/transacción."
        CUSTOMER_DATA_DESCRIPTION: str = "Datos del cliente que realiza la orden/transacción."
        PRODUCT_DATA_DESCRIPTION: str = "Datos de los productos incluidos en la orden/transacción."
        PAYMENT_DATA_DESCRIPTION: str = "Datos del pago de la orden/transacción."
        IDEMPOTENCY_KEY_DESCRIPTION: str = (
            "Clave de idempotencia creada por el cliente (navegador)."
        )
        STATUS_HISTORY_DESCRIPTION: str = (
            "Historial y registro cronológico de cambios de estado de la orden/transacción."
        )
        ORDER_NUMBER_DESCRIPTION: str = "Número de referencia de la orden/transacción."
        UNITS_DESCRIPTION: str = "Cantidad total de unidades de productos de la orden/transacción."
        SUBTOTAL_DESCRIPTION: str = "Valor neto de la orden/transacción."
        TOTAL_DESCRIPTION: str = "Valor total final de la orden/transacción."
        TAX_AMOUNT_DESCRIPTION: str = "Total de impuestos aplicados de la orden/transacción."
        UNITS_PRODUCT_DESCRIPTION: str = "Cantidad de unidades del producto de un tipo."
        SUBTOTAL_PRODUCT_DESCRIPTION: str = "Valor neto de los productos de un tipo."
        TOTAL_PRODUCT_DESCRIPTION: str = "Valor total final de los productos de un tipo."
        TAX_AMOUNT_PRODUCT_DESCRIPTION: str = (
            "Total de impuestos aplicados a los productos de un tipo."
        )
        PERCENTAGE_DESCRIPTION: str = "Porcentaje adicional para aplicar a un valor base."
        AMOUNT_DESCRIPTION: str = "Monto base al que se le va a agregar un porcentaje."

    class Errors:
        """Catálogo de mensajes de error estandarizados para la entidad `Order`."""

        IDEMPOTENCY_KEY_EXISTS: str = "Esta clave de idempotencia ya está registrado."
        PRODUCT_NOT_FOUND: str = "El producto no existe."
        SUBTOTAL_INVALID: str = (
            "El subtotal no coincide con la suma del subtotal de los productos."
        )
        UNITS_INVALID: str = (
            "Las unidades no coinciden con la suma de las unidades de los productos."
        )
        TOTAL_INVALID: str = (
            "El total de la orden no coincide con la suma del total de los productos."
        )
        TOTAL_PRODUCT_INVALID: str = (
            "El total del producto no coincide con la suma del subtotal y el impuesto."
        )
        TAX_AMOUNT_INVALID: str = (
            "El monto de impuestos no coincide con la suma de los impuestos de los productos."
        )
        TAX_AMOUNT_PRODUCT_INVALID: str = (
            "El impuesto del producto no coincide con el cálculo aplicado a su subtotal."
        )


ORDER_CONSTANTS: Final[OrderConstants] = OrderConstants()
