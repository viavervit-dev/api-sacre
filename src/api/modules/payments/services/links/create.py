import json
import logging
import smtplib
from decimal import Decimal
from uuid import UUID

import httpx
from fastapi import BackgroundTasks, status

from src.api.common.email.interfaces import IEmailService
from src.api.common.exceptions import (
    DomainRuleViolation,
    EmailDeliveryError,
    PaymentGatewayCommunicationError,
    PaymentGatewayError,
    ResourceNotFound,
)
from src.api.modules.orders.repositories.interfaces import IShoppingOrderRepository
from src.api.modules.payments.constants import PAYMENT_LINK_EMAIL_SUBJECT, PaymentType
from src.api.modules.payments.constants import ExceptionErrorMessages as PaymentException
from src.api.modules.payments.repositories.interfaces import IPaymentRepository
from src.api.modules.payments.template import PaymentTemplateRenderer
from src.api.settings.parameters import api_parameters

logger = logging.getLogger(__name__)


class CreatePaymentLinkService:
    """Servicio encargado de la creación de enlaces de pago consumiendo el servicio de pagos."""

    def __init__(
        self,
        shopping_order_repo: IShoppingOrderRepository,
        payment_repo: IPaymentRepository,
        http_client: httpx.AsyncClient,
        template_renderer: PaymentTemplateRenderer,
        email_service: IEmailService,
    ) -> None:
        self.__shopping_order_repo = shopping_order_repo
        self.__payment_repo = payment_repo
        self.__http_client = http_client
        self.__template_renderer = template_renderer
        self.__email_service = email_service

    async def execute(
        self,
        shopping_order_id: UUID,
        background_tasks: BackgroundTasks | None = None,
    ) -> None:
        """
        Envía la solicitud de creación de link al servicio de pagos, almacena la transacción
        y despacha la notificación con el enlace de pago por correo electrónico.

        Raises:
            ResourceNotFound: Si la orden de compra no existe en la base de datos.
            DomainRuleViolation: Si la orden de compra ya cuenta con un pago asociado.
            PaymentGatewayCommunicationError: Si ocurre un timeout o error de red con la pasarela.
            PaymentGatewayError: Si la pasarela de pagos rechaza la petición o responde con error.
            EmailDeliveryError: Si ocurre un error al despachar el correo de confirmación.
        """

        # Validar que la orden de compra exista en la base de datos
        shopping_order = await self.__shopping_order_repo.get_order_by_id(id=shopping_order_id)

        if not shopping_order:
            raise ResourceNotFound()

        # Ejecutar validaciones de las reglas de negocio
        await self.__run_business_validations(shopping_order_id=shopping_order_id)

        # Generamos link de pago
        payment_link = await self.__generate_payment_link(
            total=shopping_order.total,
            subtotal=shopping_order.subtotal,
            tax_amount=shopping_order.tax_amount,
            order_number=shopping_order.order_number,
            order_description=shopping_order.description,
        )
        payment_data = {
            "description": shopping_order.description,
            "type": PaymentType.PAYMENT_LINK.value,
            "status": shopping_order.status,
            "status_changed_at": None,
        }
        await self.__payment_repo.save_transaction(
            shopping_order_id=shopping_order_id,
            data=payment_data,
        )

        # Renderizar el HTML (listo para enviar por correo)
        html_body = self.__template_renderer.render_order_confirmation(
            payment_link=payment_link,
            order=shopping_order,
        )

        # Fallback en texto plano para clientes sin soporte HTML y mitigación de filtros anti-spam
        text_content = (
            f"Estimado(a) cliente,\n\n"
            f"Su orden #{shopping_order.order_number} ha sido procesada exitosamente.\n"
            f"Total a pagar: ${shopping_order.total:.2f} USD\n\n"
            f"Para completar su pago mediante nuestro enlace seguro, por favor ingrese a:\n"
            f"{payment_link}\n\n"
            f"Atentamente,\n"
            f"Sacré"
        )
        subject = PAYMENT_LINK_EMAIL_SUBJECT.format(order_number=shopping_order.order_number)

        if background_tasks is not None:
            background_tasks.add_task(
                self.__send_email,
                recipient=shopping_order.customer_data["email"],
                subject=subject,
                html_body=html_body,
                text_content=text_content,
                order_number=shopping_order.order_number,
            )
        else:
            await self.__send_email(
                recipient=shopping_order.customer_data["email"],
                subject=subject,
                html_body=html_body,
                text_content=text_content,
                order_number=shopping_order.order_number,
            )

    async def __run_business_validations(self, shopping_order_id: UUID) -> None:
        """
        Ejecuta las validaciones de las reglas de negocio previas a la creación del enlace de pago.

        Raises:
            DomainRuleViolation: Si la orden de compra ya cuenta con un pago asociado.
        """

        # Validar que la orden de compra no tenga ya un pago o enlace de pago asociado
        has_payment = await self.__payment_repo.exists_payment(
            filters={"shopping_order_id": shopping_order_id}
        )

        if has_payment:
            raise DomainRuleViolation(
                message=PaymentException.ORDER_ALREADY_HAS_PAYMENT.value,
            )

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
        order_description: str,
    ) -> str:

        try:
            response = await self.__http_client.post(
                url=api_parameters.api_payment_links,
                json={
                    "amount": self.__to_cents(amount=total),
                    "amountWithTax": self.__to_cents(amount=subtotal),
                    "tax": self.__to_cents(amount=tax_amount),
                    "clientTransactionId": order_number,
                    "reference": order_description,
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
