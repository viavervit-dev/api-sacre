from src.api.modules.orders.models.shopping_order import ShoppingOrder
from src.api.settings.templates import jinja_env


class PaymentTemplateRenderer:
    """Gestiona el renderizado de todas las plantillas HTML del módulo de pagos."""

    TEMPLATE_NAME = "order_confirmation.html"

    def __init__(self) -> None:
        self.__template = jinja_env.get_template(name=self.TEMPLATE_NAME)

    def render_order_confirmation(self, order: ShoppingOrder, payment_link: str) -> str:
        """
        Construye el contexto y renderiza la plantilla HTML. Los atributos de `ShoppingOrder`
        coinciden exactamente con el contexto esperado.
        """

        context = {
            "order_number": order.order_number,
            "customer_data": order.customer_data,
            "product_data": order.product_data,
            "subtotal": order.subtotal,
            "tax_amount": order.tax_amount,
            "total": order.total,
            "units": order.units,
            "payment_link": payment_link,
        }

        return self.__template.render(context)
