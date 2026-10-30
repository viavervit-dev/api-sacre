from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class IPaymentRepository(ABC):
    """Contrato de persistencia para operaciones sobre pagos `payments.payments`."""

    @abstractmethod
    async def save_transaction(self, shopping_order_id: UUID, data: dict[str, Any]) -> None:
        """Registra una transacción de pago asociada a una orden de compra."""

        pass

    @abstractmethod
    async def exists_payment(self, filters: dict[str, Any]) -> bool:
        """Determina si existe un pago que cumpla con los filtros proporcionados."""

        pass
