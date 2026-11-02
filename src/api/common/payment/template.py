from typing import Any

from src.api.settings.templates import jinja_env


class PaymentTemplateRenderer:
    """Gestiona el renderizado de todas las plantillas HTML del módulo de pagos."""

    def render_order_confirmation(self, data: dict[str, Any], payment_link: str) -> str:
        """
        Construye el contexto y renderiza la plantilla HTML de confirmación de la
        órden/transacción.
        """

        template = jinja_env.get_template(name="order_confirmation.html")
        context = {
            "order_number": data["order_number"],
            "customer_data": data["customer_data"],
            "product_data": data["product_data"],
            "subtotal": data["subtotal"],
            "tax_amount": data["tax_amount"],
            "total": data["total"],
            "units": data["units"],
            "payment_link": payment_link,
        }

        return template.render(context)
