from collections.abc import Sequence

from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.models.user import User
from src.api.modules.inventory.dto import ReadWholesalerProductSummaryDTO
from src.api.modules.inventory.repositories.interfaces import IWholesalerProductRepository


class GetListProductWholesalerService:
    """Servicio encargado de la consulta de productos de clientes mayoristas."""

    def __init__(self, wholesaler_product_repo: IWholesalerProductRepository) -> None:
        self.__wholesaler_product_repo = wholesaler_product_repo

    async def get_list(
        self,
        user: User,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[ReadWholesalerProductSummaryDTO], int]:
        """
        Obtiene una lista paginada de productos de clientes mayoristas según filtros y nivel de
        visibilidad.
        """

        if user.role == UserRoles.ADMINISTRATOR.value:
            return await self.__get_all_products(offset=offset, limit=limit)

        # Tanto usuarios autenticados con rol diferente
        return await self.__get_active_products(offset=offset, limit=limit)

    async def __get_active_products(
        self,
        offset: int,
        limit: int,
    ) -> tuple[list[ReadWholesalerProductSummaryDTO], int]:
        """Consulta y serializa todos los productos activos de los clientes mayoristas."""

        result = []

        products, total_items = await self.__wholesaler_product_repo.get_active_products(
            offset=offset,
            limit=limit,
        )

        if not products:
            return [], 0

        for product in products:
            dto = ReadWholesalerProductSummaryDTO.model_construct(**product.to_dict())
            result.append(dto)

        return result, total_items

    async def __get_all_products(
        self,
        offset: int,
        limit: int,
    ) -> tuple[list[ReadWholesalerProductSummaryDTO], int]:
        """Consulta y serializa todos los productos de los clientes mayoristas."""

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
