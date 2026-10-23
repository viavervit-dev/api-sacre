from abc import ABC, abstractmethod
from typing import Any

from src.api.modules.orders.models.order import ShoppingOrder


class IShoppingOrderRepository(ABC):
    """Contrato de persistencia para operaciones sobre órdenes (`orders.orders`)."""

    @abstractmethod
    async def create_order(self, data: dict[str, Any]) -> ShoppingOrder:
        """Crea una nueva orden de compra en la base de datos."""

        pass

    @abstractmethod
    async def exists_order(self, filters: dict[str, Any]) -> bool:
        """Verifica si existe una orden de compra que coincida con los filtros especificados."""

        pass
