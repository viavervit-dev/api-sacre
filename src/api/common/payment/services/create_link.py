import json
import logging
import smtplib
from decimal import Decimal
from typing import Any

import httpx
from fastapi import status

from src.api.common.email.interfaces import IEmailService
from src.api.common.exceptions import (
    EmailDeliveryError,
    PaymentGatewayCommunicationError,
    PaymentGatewayError,
)
from src.api.common.payment.constants import PAYMENT_LINK_EMAIL_SUBJECT
from src.api.common.payment.constants import ExceptionErrorMessages as PaymentException
from src.api.common.payment.template import PaymentTemplateRenderer
from src.api.settings.parameters import api_parameters

logger = logging.getLogger(__name__)


class CreatePaymentLinkService:
    """Servicio encargado de la creación de enlaces de pago consumiendo el servicio de pagos."""

    def __init__(
        self,
        http_client: httpx.AsyncClient,
        template_renderer: PaymentTemplateRenderer,
        email_service: IEmailService,
    ) -> None:
        self.__http_client = http_client
        self.__template_renderer = template_renderer
        self.__email_service = email_service

    async def create_payment_link(self, order_data: dict[str, Any]) -> str:
        """
        Envía la solicitud de creación de link al servicio de pagos, almacena la transacción
        y despacha la notificación con el enlace de pago al correo electrónico del cliente.

        Raises:
            DomainRuleViolation: Si la orden de compra ya cuenta con un pago asociado.
            PaymentGatewayCommunicationError: Si ocurre un timeout o error de red con la pasarela.
            PaymentGatewayError: Si la pasarela de pagos rechaza la petición o responde con error.
            EmailDeliveryError: Si ocurre un error al despachar el correo de confirmación.
        """

        # Generamos link de pago
        payment_link = await self.__generate_payment_link(
            total=order_data["total"],
            subtotal=order_data["subtotal"],
            tax_amount=order_data["tax_amount"],
            order_number=order_data["order_number"],
        )

        # Renderizar el HTML (listo para enviar por correo)
        html_body = self.__template_renderer.render_order_confirmation(
            payment_link=payment_link,
            data=order_data,
        )

        # Enviamos notificación al cliente
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
        await self.__send_email(
            recipient=order_data["customer_data"]["email"],
            order_number=order_data["order_number"],
            text_content=text_content,
            html_body=html_body,
            subject=subject,
        )

        return payment_link

    async def __send_email(
        self,
        recipient: str,
        subject: str,
        html_body: str,
        text_content: str,
        order_number: str,
    ) -> None:
        """Despacha el correo de confirmación con captura segura y registro de excepciones."""

        try:
            await self.__email_service.send_email(
                recipient=recipient,
                subject=subject,
                html_content=html_body,
                text_content=text_content,
            )
        except (smtplib.SMTPException, smtplib.SMTPRecipientsRefused) as exc:
            logger.error("Error al despachar un correo electrónico: %s", exc)

            raise EmailDeliveryError(
                message=PaymentException.DELIVERY_ERROR.value,
            ) from exc
        except Exception as exc:
            logger.error(
                "Error al enviar correo de confirmación para la orden %s a %s: %s",
                order_number,
                self.__mask_email(email=recipient),
                exc,
                exc_info=True,
            )

    @staticmethod
    def __mask_email(email: str) -> str:
        """Enmascara una dirección de correo para proteger datos personales en logs."""

        if "@" not in email:
            return "***"

        local, domain = email.split("@", 1)
        visible_chars = min(2, len(local))

        return f"{local[:visible_chars]}***@{domain}"

    async def __generate_payment_link(
        self,
        total: Decimal,
        subtotal: Decimal,
        tax_amount: Decimal,
        order_number: str,
    ) -> str:

        try:
            response = await self.__http_client.post(
                url=api_parameters.api_payment_links,
                json={
                    "amount": self.__to_cents(amount=total),
                    "amountWithTax": self.__to_cents(amount=subtotal),
                    "tax": self.__to_cents(amount=tax_amount),
                    "clientTransactionId": order_number,
                    "storeId": api_parameters.api_payment_store_id,
                    "currency": "USD",
                    "oneTime": True,  # Se configura el link para un solo uso
                    "isAmountEditable": False,
                },
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_parameters.api_payment_key}",
                },
            )
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            logger.error("Timeout con la pasarela para la orden %s: %s", order_number, exc)

            raise PaymentGatewayCommunicationError(
                message=PaymentException.GATEWAY_TIMEOUT.value,
            ) from exc
        except httpx.RequestError as exc:
            logger.error("Error de red con el servicio de pagos %s: %s", order_number, exc)

            raise PaymentGatewayCommunicationError(
                message=PaymentException.GATEWAY_CONNECTION_ERROR.value,
            ) from exc
        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code
            raw_body = exc.response.text[:500]

            if status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN):
                logger.critical(
                    "Error de autenticación o de permisos con el servicio de pagos (%s): %s",
                    status_code,
                    raw_body,
                )

                raise PaymentGatewayError(
                    message=PaymentException.GATEWAY_CONFIG_ERROR.value,
                ) from exc
            if status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
                logger.error(
                    "Error 5xx del servicio de pagos %s (status %s): %s",
                    order_number,
                    status_code,
                    raw_body,
                )

                raise PaymentGatewayError(
                    message=PaymentException.GATEWAY_UNAVAILABLE.value,
                ) from exc

            logger.warning(
                "El servicio de pago rechazó la petición %s (status %s): %s",
                order_number,
                status_code,
                raw_body,
            )

            raise PaymentGatewayError(
                message=PaymentException.GATEWAY_REJECTED.value,
            ) from exc

        try:
            payment_link = response.json()
        except (json.JSONDecodeError, ValueError) as exc:
            logger.error(
                "Respuesta no JSON de la pasarela para orden %s: %s",
                order_number,
                response.text[:200],
            )

            raise PaymentGatewayError(
                message=PaymentException.GATEWAY_INVALID_RESPONSE.value,
            ) from exc

        return str(payment_link)

    @staticmethod
    def __to_cents(amount: Decimal) -> int:
        """
        Convierte un monto en dólares a su valor exacto en centavos. Garantiza que no se realicen
        aproximaciones ni redondeos por arriba o por abajo.
        """

        cents = amount * 100

        # Validamos que no existan más de dos decimales
        if cents % 1 != 0:
            raise ValueError(
                f"El valor '{amount}' contiene más de dos decimales. "
                "No se permiten aproximaciones en montos monetarios."
            )

        return int(cents)
