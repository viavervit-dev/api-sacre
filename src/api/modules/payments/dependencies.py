from typing import Annotated

import httpx
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.common.email.dependencies import email_service
from src.api.common.email.service import EmailService
from src.api.modules.orders.dependencies import (
    ShoppingOrderRepository,
    shopping_order_repository,
)
from src.api.modules.payments.repositories.payment import PaymentRepository
from src.api.modules.payments.services.links.create import CreatePaymentLinkService
from src.api.modules.payments.template import PaymentTemplateRenderer
from src.api.settings.database import db_session
from src.api.settings.http_client import http_client


def payment_repository(
    db: Annotated[AsyncSession, Depends(db_session)],
) -> PaymentRepository:
    """Provee una instancia del repositorio de la gestión de pagos de clientes."""

    return PaymentRepository(db=db)


def create_payment_link_service(
    shopping_order_repo: Annotated[ShoppingOrderRepository, Depends(shopping_order_repository)],
    payment_repo: Annotated[PaymentRepository, Depends(payment_repository)],
    http_client: Annotated[httpx.AsyncClient, Depends(http_client)],
    email_service_instance: Annotated[EmailService, Depends(email_service)],
) -> CreatePaymentLinkService:
    """Provee una instancia del servicio de creación de links de pago."""

    return CreatePaymentLinkService(
        shopping_order_repo=shopping_order_repo,
        payment_repo=payment_repo,
        http_client=http_client,
        template_renderer=PaymentTemplateRenderer(),
        email_service=email_service_instance,
    )
