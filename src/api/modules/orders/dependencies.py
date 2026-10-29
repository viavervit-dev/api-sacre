from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.common.utils import FinancialCalculationsMixin
from src.api.modules.auth.dependencies import UserRepository, user_repository
from src.api.modules.inventory.dependencies import ProductRepository, product_repository
from src.api.modules.orders.repositories.shopping_order import ShoppingOrderRepository
from src.api.modules.orders.services.shopping.create import CreateOrderCustomerWholesaleService
from src.api.settings.database import db_session


def shopping_order_repository(
    db: Annotated[AsyncSession, Depends(db_session)],
) -> ShoppingOrderRepository:
    """Provee una instancia del repositorio de ordenes de compra."""

    return ShoppingOrderRepository(db=db)


def financial_calculations_service() -> type[FinancialCalculationsMixin]:
    """
    Provee una instancia del servicio que provee métodos auxiliares y cálculos matemáticos
    financieros.
    """

    return FinancialCalculationsMixin


def create_order_customer_wholesale_service(
    product_repo: Annotated[ProductRepository, Depends(product_repository)],
    shopping_order_repo: Annotated[ShoppingOrderRepository, Depends(shopping_order_repository)],
    user_repo: Annotated[UserRepository, Depends(user_repository)],
) -> CreateOrderCustomerWholesaleService:
    """
    Provee una instancia del servicio encargado de la creación de órdenes de compra
    para clientes mayoristas.
    """

    return CreateOrderCustomerWholesaleService(
        shopping_order_repo=shopping_order_repo,
        product_repo=product_repo,
        user_repo=user_repo,
    )
