from typing import Annotated

import httpx
from fastapi import Depends

from src.api.common.email.dependencies import email_service
from src.api.common.email.service import EmailService
from src.api.common.payment.services.create_link import CreatePaymentLinkService
from src.api.common.payment.template import PaymentTemplateRenderer
from src.api.settings.http_client import http_client


def create_payment_link_service(
    http_client: Annotated[httpx.AsyncClient, Depends(http_client)],
    email_service_instance: Annotated[EmailService, Depends(email_service)],
) -> CreatePaymentLinkService:
    """Provee una instancia del servicio de creación de links de pago."""

    return CreatePaymentLinkService(
        http_client=http_client,
        template_renderer=PaymentTemplateRenderer(),
        email_service=email_service_instance,
    )
