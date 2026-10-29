from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class IPaymentRepository(ABC):
    """Contrato de persistencia para operaciones sobre pagos `payments.payments`."""

    @abstractmethod
    async def save_transaction(self, shopping_order_id: UUID, data: dict[str, Any]) -> None:
        """Registra una transacción de pago asociada a una orden de compra."""

        pass
