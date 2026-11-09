from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any
from uuid import UUID

from src.api.modules.orders.models import Order


class IOrderRepository(ABC):
    """Contrato de persistencia para operaciones sobre órdenes/transacciones (`orders.orders`)."""

    @abstractmethod
    async def get_order_by_id(self, id: UUID, order_type: str) -> Order | None:
        """Obtiene una órden/transacción por su identificador único."""

        pass

    @abstractmethod
    async def get_list_orders(
        self,
        offset: int,
        limit: int,
        order_type: str,
    ) -> tuple[Sequence[Order], int]:
        """Obtiene una lista de órdenes/transacciones y el total de registros encontrados."""

        pass

    @abstractmethod
    async def create_order(self, data: dict[str, Any]) -> Order:
        """Crea una nueva órden/transacción en la base de datos."""

        pass

    @abstractmethod
    async def exists_order(self, filters: dict[str, Any]) -> bool:
        """Verifica si existe una órden/transacción que coincida con los filtros especificados."""

        pass

    @abstractmethod
    async def get_next_order_number(self) -> str:
        """Genera el siguiente número de referencia de una órden/transacción."""

        pass
