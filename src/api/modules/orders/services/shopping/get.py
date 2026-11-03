from uuid import UUID

from src.api.common.exceptions import ResourceNotFound
from src.api.modules.orders.dto import (
    ReadCustomerDataDTO,
    ReadOrderDTO,
    ReadPaymentDataDTO,
    ReadProductDataDTO,
)
from src.api.modules.orders.repositories.interfaces import IOrderRepository


class GetOrderService:
    """Servicio encargado de la consulta y obtención del detalle de una orden de compra."""

    def __init__(self, order_repo: IOrderRepository) -> None:
        self.__order_repo = order_repo

    async def get(self, order_id: UUID) -> ReadOrderDTO:
        """
        Obtiene el detalle completo de una orden de compra por su identificador único.

        Raises:
            ResourceNotFound: Si la orden de compra no existe en la base de datos.
        """

        # Validar que la orden exista
        order = await self.__order_repo.get_order_by_id(id=order_id)

        if not order:
            raise ResourceNotFound()

        # Extraer estructuras anidadas para instanciar el DTO de respuesta
        order_data = order.to_dict()
        customer_data = order_data.pop("customer_data")
        product_data = order_data.pop("product_data")
        payment_data = order_data.pop("payment_data")

        return ReadOrderDTO.model_construct(
            **order_data,
            customer_data=ReadCustomerDataDTO.model_construct(**customer_data),
            product_data=[ReadProductDataDTO.model_construct(**p) for p in product_data],
            payment_data=ReadPaymentDataDTO.model_construct(**payment_data),
        )
