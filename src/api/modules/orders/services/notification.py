import logging
from typing import Any

from src.api.common.email.service import EmailService
from src.api.common.exceptions import EmailConfigurationError, EmailDeliveryError
from src.api.common.payment.constants import PAYMENT_LINK_EMAIL_SUBJECT
from src.api.common.payment.constants import ExceptionErrorMessages as PaymentException
from src.api.settings.templates import jinja_env

logger = logging.getLogger(__name__)


class OrderNotificationService:
    """Servicio encargado de las notificaciones al cliente sobre órdenes de compra."""

    def __init__(self, email_service: EmailService) -> None:
        self.__email_service = email_service

    async def send_order_payment_link(self, order_data: dict[str, Any], payment_link: str) -> None:
        """
        Renderiza y despacha el correo de confirmación con el enlace de pago.

        Raises:
            EmailDeliveryError: Si ocurre un error al despachar el correo.
            EmailConfigurationError: Si el servicio SMTP no está configurado adecuadamente.
        """

        template = jinja_env.get_template(name="order_confirmation.html")
        context = {
            "order_number": order_data["order_number"],
            "customer_data": order_data["customer_data"],
            "product_data": order_data["product_data"],
            "subtotal": order_data["subtotal"],
            "tax_amount": order_data["tax_amount"],
            "total": order_data["total"],
            "units": order_data["units"],
            "payment_link": payment_link,
        }
        html_body = template.render(context)

        text_content = (
            f"Estimado(a) cliente,\n\n"
            f"Su orden #{order_data['order_number']} ha sido procesada exitosamente.\n"
            f"Total a pagar: ${order_data['total']:.2f} USD\n\n"
            f"Para completar su pago mediante nuestro enlace seguro, por favor ingrese a:\n"
            f"{payment_link}\n\n"
            f"Atentamente,\n"
            f"Sacré"
        )
        subject = PAYMENT_LINK_EMAIL_SUBJECT.format(order_number=order_data["order_number"])
        recipient = order_data["customer_data"]["email"]

        try:
            await self.__email_service.send_email(
                recipient=recipient,
                subject=subject,
                html_content=html_body,
                text_content=text_content,
            )
        except EmailDeliveryError, EmailConfigurationError:
            # Excepciones de dominio tipadas lanzadas por EmailService: se relanzan directamente
            raise
        except Exception as exc:
            logger.error(
                "Fallo inesperado al enviar correo para la orden %s a %s: %s",
                order_data["order_number"],
                self.__mask_email(recipient),
                exc,
                exc_info=True,
            )

            raise EmailDeliveryError(message=PaymentException.DELIVERY_ERROR.value) from exc

    @staticmethod
    def __mask_email(email: str) -> str:
        """Enmascara una dirección de correo para su registro seguro en logs."""

        if "@" not in email:
            return "***"

        local, domain = email.split("@", 1)
        visible = min(2, len(local))

        return f"{local[:visible]}***@{domain}"
