from typing import Annotated

from fastapi import Depends

from src.api.common.email.dependencies import EmailService, email_service
from src.api.common.payment.dependencies import create_payment_link_service
from src.api.common.payment.services import CreatePaymentLinkService
from src.api.common.utils import FinancialCalculationsMixin
from src.api.modules.auth.dependencies import UserRepository, user_repository
from src.api.modules.inventory.dependencies import (
    ProductRepository,
    WholesalerProductRepository,
    product_repository,
    wholesaler_product_repository,
)
from src.api.modules.orders.repositories import OrderRepository
from src.api.modules.orders.services import OrderNotificationService
from src.api.modules.orders.services.purchase import (
    CreatePurchaseOrderWholesalerService,
    GetListPurchaseOrderService,
    GetPurchaseOrderService,
)
from src.api.settings.database import DBSession


def order_repository(db: DBSession) -> OrderRepository:
    """Provee una instancia del repositorio de ordenes de compra."""

    return OrderRepository(db=db)


def financial_calculations_service() -> type[FinancialCalculationsMixin]:
    """
    Provee una instancia del servicio que provee métodos auxiliares y cálculos matemáticos
    financieros.
    """

    return FinancialCalculationsMixin


def get_list_purchase_order_service(
    order_repo: Annotated[OrderRepository, Depends(order_repository)],
) -> GetListPurchaseOrderService:
    """
    Provee una instancia del servicio encargado de la consulta y serialización de órdenes
    de compra.
    """

    return GetListPurchaseOrderService(order_repo=order_repo)


def get_purchase_order_service(
    order_repo: Annotated[OrderRepository, Depends(order_repository)],
) -> GetPurchaseOrderService:
    """
    Provee una instancia del servicio encargado de la consulta y serialización de órdenes
    de compra.
    """

    return GetPurchaseOrderService(order_repo=order_repo)


def notification_service(
    email_service: Annotated[EmailService, Depends(email_service)],
) -> OrderNotificationService:
    """
    Provee una instancia del servicio encargado de despachar notificaciones al cliente sobre
    órdenes de compra
    """

    return OrderNotificationService(email_service=email_service)


def create_purchase_order_wholesaler_service(
    payment_service: Annotated[CreatePaymentLinkService, Depends(create_payment_link_service)],
    notification_service: Annotated[OrderNotificationService, Depends(notification_service)],
    order_repo: Annotated[OrderRepository, Depends(order_repository)],
    user_repo: Annotated[UserRepository, Depends(user_repository)],
    product_repo: Annotated[ProductRepository, Depends(product_repository)],
    wholesaler_product_repo: Annotated[
        WholesalerProductRepository, Depends(wholesaler_product_repository)
    ],
) -> CreatePurchaseOrderWholesalerService:
    """
    Provee una instancia del servicio encargado de la creación de órdenes de compra
    para clientes mayoristas.
    """

    return CreatePurchaseOrderWholesalerService(
        payment_service=payment_service,
        wholesaler_product_repo=wholesaler_product_repo,
        notification_service=notification_service,
        product_repo=product_repo,
        order_repo=order_repo,
        user_repo=user_repo,
    )
