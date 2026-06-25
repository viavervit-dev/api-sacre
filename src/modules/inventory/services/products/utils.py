from decimal import ROUND_HALF_UP, Decimal

from src.common.constants import TWO_DECIMAL_PLACES


class ProductServiceBase:
    """
    Servicio básico para utilidades de productos. Esta clase proporciona métodos auxiliares
    compartidos que utilizan los servicios de productos.
    """

    @staticmethod
    def _calculate_sale_price(
        price_neto: Decimal,
        iva: Decimal,
        profit_margin: Decimal,
    ) -> Decimal:
        """Calcula el precio de venta a partir del precio neto, IVA y margen de beneficio."""

        raw_price_sale = price_neto * (Decimal("1.0000") + profit_margin)
        raw_price_sale = raw_price_sale * (Decimal("1.0000") + iva)

        return raw_price_sale.quantize(
            exp=TWO_DECIMAL_PLACES,
            rounding=ROUND_HALF_UP,
        )
