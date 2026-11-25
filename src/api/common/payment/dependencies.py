from typing import Annotated

from fastapi import Depends

from src.api.common.payment.services import CreatePaymentLinkService
from src.api.settings.http import HTTPClientDep


def create_payment_link_service(http_client: HTTPClientDep) -> CreatePaymentLinkService:
    """Provee una instancia del servicio de creación de links de pago."""

    return CreatePaymentLinkService(http_client=http_client)


CreatePaymentLinkServiceDep = Annotated[
    CreatePaymentLinkService, Depends(create_payment_link_service)
]
