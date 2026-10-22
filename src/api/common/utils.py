from collections.abc import Iterable
from decimal import ROUND_HALF_UP, Decimal

from src.api.common.constants import TAX_PERCENTAGE, TWO_DECIMAL_PLACES


class FinancialCalculationsMixin:
    """Clase que provee métodos auxiliares y cálculos matemáticos financieros."""

    @staticmethod
    def sum(values: Iterable[Decimal]) -> Decimal:
        """
        Suma una secuencia o iterable de objetos Decimal y redondea el resultado a dos decimales.
        """

        total = sum(values, start=Decimal("0.00"))

        return total.quantize(
            exp=TWO_DECIMAL_PLACES,
            rounding=ROUND_HALF_UP,
        )

    @staticmethod
    def calculate_tax_amount(amount: Decimal) -> Decimal:
        """Calcula el monto del impuesto sobre un valor base y lo redondea a dos decimales."""

        tax_amount = amount * TAX_PERCENTAGE

        return tax_amount.quantize(
            exp=TWO_DECIMAL_PLACES,
            rounding=ROUND_HALF_UP,
        )

    @staticmethod
    def add_percentage(base_value: Decimal, percentage: Decimal) -> Decimal:
        """Aplica un porcentaje adicional a un valor base y lo redondea a dos decimales."""

        total = base_value * (Decimal("1") + percentage)

        return total.quantize(
            exp=TWO_DECIMAL_PLACES,
            rounding=ROUND_HALF_UP,
        )

    @staticmethod
    def calculate_sale_price_product(price_neto: Decimal, profit_margin: Decimal) -> Decimal:
        """
        Calcula el precio de venta final de un producto aplicando margen de ganancia e IVA
        y lo redondea a dos decimales.
        """

        raw_price_sale = (
            price_neto * (Decimal("1") + profit_margin) * (Decimal("1") + TAX_PERCENTAGE)
        )

        return raw_price_sale.quantize(
            exp=TWO_DECIMAL_PLACES,
            rounding=ROUND_HALF_UP,
        )

    @staticmethod
    def multiply(value: Decimal, multiplier: int) -> Decimal:
        """
        Multiplica un valor Decimal por un número entero y redondea el resultado a dos decimales.
        """

        total = value * multiplier

        return total.quantize(
            exp=TWO_DECIMAL_PLACES,
            rounding=ROUND_HALF_UP,
        )
