import asyncio
import json
import logging
from decimal import Decimal
from typing import Any

import httpx
from fastapi import status

from src.api.common.exceptions import (
    PaymentGatewayCommunicationError,
    PaymentGatewayError,
)
from src.api.common.payment.constants import ExceptionErrorMessages as PaymentException
from src.api.settings.parameters import api_parameters

logger = logging.getLogger(__name__)


class CreatePaymentLinkService:
    """Servicio encargado de la creación de enlaces de pago consumiendo el servicio de pagos."""

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self.__http_client = http_client

    async def create_payment_link(self, order_data: dict[str, Any]) -> str:
        """
        Envía la solicitud de creación de link al servicio de pagos.

        Raises:
            PaymentGatewayCommunicationError: Si ocurre un timeout o error de red con la pasarela.
            PaymentGatewayError: Si la pasarela de pagos rechaza la petición o responde con error.
        """

        # Generamos link de pago
        payment_link = await self.__generate_payment_link(
            total=order_data["total"],
            subtotal=order_data["subtotal"],
            tax_amount=order_data["tax_amount"],
            order_number=order_data["order_number"],
        )

        return payment_link

    async def __generate_payment_link(
        self,
        total: Decimal,
        subtotal: Decimal,
        tax_amount: Decimal,
        order_number: str,
    ) -> str:
        """
        Construye el payload en centavos y realiza la petición HTTP al servicio de pagos
        para generar y retornar el enlace de pago.

        Raises:
            ValueError: Si algún monto contiene más de dos decimales.
            PaymentGatewayCommunicationError: Si ocurre un timeout o error de red con la pasarela.
            PaymentGatewayError: Si la pasarela responde con error HTTP o un JSON inválido.
        """

        try:
            async with asyncio.timeout(delay=15.0):
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
        except (httpx.TimeoutException, TimeoutError) as exc:
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
