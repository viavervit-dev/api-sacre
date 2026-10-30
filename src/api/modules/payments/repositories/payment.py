from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.payments.models.payment import Payment
from src.api.modules.payments.repositories.interfaces import IPaymentRepository


class PaymentRepository(IPaymentRepository):
    """Repositorio SQLAlchemy para la gestión de pagos de clientes en `payments.payments`."""

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def save_transaction(self, shopping_order_id: UUID, data: dict[str, Any]) -> None:

        instance = Payment(shopping_order_id=shopping_order_id, **data)
        self.__db.add(instance)
        await self.__db.flush()

    async def exists_payment(self, filters: dict[str, Any]) -> bool:

        stmt = select(Payment.id).filter_by(**filters)
        result = await self.__db.scalar(select(stmt.exists()))

        return bool(result)
