from collections.abc import Sequence

from src.api.modules.inventory.dto import ReadWholesalerProductSummaryDTO
from src.api.modules.inventory.repositories.interfaces import IWholesalerProductRepository


class GetListProductWholesalerService:
    """Servicio encargado de la consulta de productos de clientes mayoristas."""

    def __init__(self, wholesaler_product_repo: IWholesalerProductRepository) -> None:
        self.__wholesaler_product_repo = wholesaler_product_repo

    async def get_list(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[ReadWholesalerProductSummaryDTO], int]:
        """Obtiene una lista paginada de productos de clientes mayoristas."""

        result = []

        products, total_items = await self.__wholesaler_product_repo.get_all_products(
            offset=offset,
            limit=limit,
        )

        if not products:
            return [], 0

        for product in products:
            dto = ReadWholesalerProductSummaryDTO.model_construct(**product.to_dict())
            result.append(dto)

        return result, total_items
