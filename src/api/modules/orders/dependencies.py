from typing import Annotated

from fastapi import Depends

from src.api.common.email.dependencies import EmailServiceDep
from src.api.common.payment.dependencies import CreatePaymentLinkServiceDep
from src.api.common.utils import FinancialCalculationsMixin
from src.api.modules.auth.dependencies import UserRepositoryDep
from src.api.modules.inventory.dependencies import (
    ProductRepositoryDep,
    WholesalerProductRepositoryDep,
)
from src.api.modules.orders.repositories import OrderRepository
from src.api.modules.orders.services import OrderNotificationService
from src.api.modules.orders.services.purchase import (
    CreateOrderWholesalerService,
    GetListPurchaseOrderService,
    GetPurchaseOrderService,
)
from src.api.settings.database import DBSessionDep


def order_repository(db: DBSessionDep) -> OrderRepository:
    """Provee una instancia del repositorio de ordenes de compra."""

    return OrderRepository(db=db)


OrderRepositoryDep = Annotated[OrderRepository, Depends(order_repository)]


def financial_calculations_service() -> type[FinancialCalculationsMixin]:
    """
    Provee una instancia del servicio que provee métodos auxiliares y cálculos matemáticos
    financieros.
    """

    return FinancialCalculationsMixin


FinancialCalculationsDep = Annotated[
    type[FinancialCalculationsMixin], Depends(financial_calculations_service)
]


def get_list_purchase_order_service(order_repo: OrderRepositoryDep) -> GetListPurchaseOrderService:
    """
    Provee una instancia del servicio encargado de la consulta y serialización de órdenes
    de compra.
    """

    return GetListPurchaseOrderService(order_repo=order_repo)


GetListPurchaseOrderServiceDep = Annotated[
    GetListPurchaseOrderService, Depends(get_list_purchase_order_service)
]


def get_purchase_order_service(order_repo: OrderRepositoryDep) -> GetPurchaseOrderService:
    """
    Provee una instancia del servicio encargado de la consulta y serialización de órdenes
    de compra.
    """

    return GetPurchaseOrderService(order_repo=order_repo)


GetPurchaseOrderServiceDep = Annotated[
    GetPurchaseOrderService, Depends(get_purchase_order_service)
]


def notification_service(email_service: EmailServiceDep) -> OrderNotificationService:
    """
    Provee una instancia del servicio encargado de despachar notificaciones al cliente sobre
    órdenes de compra
    """

    return OrderNotificationService(email_service=email_service)


OrderNotificationServiceDep = Annotated[OrderNotificationService, Depends(notification_service)]


def create_purchase_order_wholesaler_service(
    create_payment_link_service: CreatePaymentLinkServiceDep,
    order_repo: OrderRepositoryDep,
    user_repo: UserRepositoryDep,
    product_repo: ProductRepositoryDep,
    wholesaler_product_repo: WholesalerProductRepositoryDep,
) -> CreateOrderWholesalerService:
    """
    Provee una instancia del servicio encargado de la creación de órdenes de compra
    para clientes mayoristas.
    """

    return CreateOrderWholesalerService(
        create_payment_link_service=create_payment_link_service,
        wholesaler_product_repo=wholesaler_product_repo,
        product_repo=product_repo,
        order_repo=order_repo,
        user_repo=user_repo,
    )


CreateOrderWholesalerServiceDep = Annotated[
    CreateOrderWholesalerService, Depends(create_purchase_order_wholesaler_service)
]
