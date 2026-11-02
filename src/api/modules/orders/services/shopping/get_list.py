from collections.abc import Sequence

from src.api.modules.orders.constants import OrderDescription
from src.api.modules.orders.dto import (
    ReadCustomerDataSummaryDTO,
    ReadOrderSummaryDTO,
    ReadPaymentDataDTO,
)
from src.api.modules.orders.repositories.interfaces import IOrderRepository


class GetListOrderService:
    """Servicio encargado de la consulta y serialización de órdenes de compra."""

    def __init__(self, order_repo: IOrderRepository) -> None:
        self.__order_repo = order_repo

    async def get_list(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[ReadOrderSummaryDTO], int]:
        """Obtiene una lista paginada de órdenes de compra y el total de registros."""

        orders, total_items = await self.__order_repo.get_list_orders(
            order_type=OrderDescription.SHOPPING_ORDER.value,
            offset=offset,
            limit=limit,
        )

        if not orders:
            return [], 0

        result = []

        for order in orders:
            order_data = order.to_dict()
            customer_data = order_data.pop("customer_data") or {}
            payment_data = order_data.pop("payment_data") or {}
            dto = ReadOrderSummaryDTO.model_construct(
                **order_data,
                customer_data=ReadCustomerDataSummaryDTO.model_construct(**customer_data),
                payment_data=ReadPaymentDataDTO.model_construct(**payment_data),
            )
            result.append(dto)

        return result, total_items
