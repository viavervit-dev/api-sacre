from typing import Annotated

import httpx
from fastapi import Depends

from src.api.common.payment.services import CreatePaymentLinkService
from src.api.settings.http_client import http_client


def create_payment_link_service(
    http_client: Annotated[httpx.AsyncClient, Depends(http_client)],
) -> CreatePaymentLinkService:
    """Provee una instancia del servicio de creación de links de pago."""

    return CreatePaymentLinkService(http_client=http_client)
