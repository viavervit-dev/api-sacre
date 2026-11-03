from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.common.payment.dependencies import create_payment_link_service
from src.api.common.payment.services.create_link import CreatePaymentLinkService
from src.api.common.utils import FinancialCalculationsMixin
from src.api.modules.auth.dependencies import UserRepository, user_repository
from src.api.modules.inventory.dependencies import ProductRepository, product_repository
from src.api.modules.orders.repositories.order import OrderRepository
from src.api.modules.orders.services.purchase.create_order_whosaler import (
    CreatePurchaseOrderWholesalerService,
)
from src.api.modules.orders.services.purchase.get import GetPurchaseOrderService
from src.api.modules.orders.services.purchase.get_list import GetListPurchaseOrderService
from src.api.settings.database import db_session


def order_repository(db: Annotated[AsyncSession, Depends(db_session)]) -> OrderRepository:
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


def create_purchase_order_wholesaler_service(
    product_repo: Annotated[ProductRepository, Depends(product_repository)],
    order_repo: Annotated[OrderRepository, Depends(order_repository)],
    payment_service: Annotated[CreatePaymentLinkService, Depends(create_payment_link_service)],
    user_repo: Annotated[UserRepository, Depends(user_repository)],
) -> CreatePurchaseOrderWholesalerService:
    """
    Provee una instancia del servicio encargado de la creación de órdenes de compra
    para clientes mayoristas.
    """

    return CreatePurchaseOrderWholesalerService(
        payment_service=payment_service,
        product_repo=product_repo,
        order_repo=order_repo,
        user_repo=user_repo,
    )
