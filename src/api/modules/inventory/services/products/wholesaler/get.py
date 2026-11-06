from uuid import UUID

from src.api.common.exceptions import ResourceNotFound
from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.repositories.interfaces import IUserRepository
from src.api.modules.inventory.dto import ReadWholesalerProductSummaryDTO
from src.api.modules.inventory.repositories.interfaces import IWholesalerProductRepository


class GetProductsWholesalerService:
    """Servicio encargado de la consulta y serialización de productos de un mayorista."""

    def __init__(
        self,
        user_repo: IUserRepository,
        wholesaler_product_repo: IWholesalerProductRepository,
    ) -> None:
        self.__wholesaler_product_repo = wholesaler_product_repo
        self.__user_repo = user_repo

    async def get_products(
        self,
        wholesaler_id: UUID,
        offset: int,
        limit: int,
    ) -> tuple[list[ReadWholesalerProductSummaryDTO], int]:
        """
        Obtiene una lista paginada de los productos de un cliente mayorista.

        Raises:
            ResourceNotFound: Si el cliente mayorista no existe en la base de datos.
        """

        # Validamos que el mayorista exista en la base de datos
        user = await self.__user_repo.get_user(
            filters={"id": wholesaler_id, "role": UserRoles.WHOLESALER.value},
            load_permissions=False,
        )

        if not user:
            raise ResourceNotFound()

        # Consultamos los productos del mayorista en la base de datos
        products, total_items = await self.__wholesaler_product_repo.get_products_by_wholesaler(
            wholesaler_id=wholesaler_id,
            offset=offset,
            limit=limit,
        )

        if not products:
            return [], 0

        result = []

        for product in products:
            dto = ReadWholesalerProductSummaryDTO.model_construct(**product.to_dict())
            result.append(dto)

        return result, total_items
