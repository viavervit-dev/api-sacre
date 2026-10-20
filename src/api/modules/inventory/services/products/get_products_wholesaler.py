from uuid import UUID

from src.api.common.exceptions import ResourceNotFound
from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.repositories.interfaces import IUserRepository
from src.api.modules.inventory.dto import ReadProductPrivateDTO
from src.api.modules.inventory.repositories.interfaces import IProductRepository


class GetProductsWholesalerService:
    """Servicio encargado de la consulta y serialización de productos de un mayorista."""

    def __init__(self, user_repo: IUserRepository, product_repo: IProductRepository) -> None:
        self.__product_repo = product_repo
        self.__user_repo = user_repo

    async def get_products(
        self,
        wholesaler_id: UUID,
        offset: int,
        limit: int,
    ) -> tuple[list[ReadProductPrivateDTO], int]:
        """
        Obtiene una lista paginada de los productos exclusivos de un cliente mayorista.

        Raises:
            ResourceNotFound: Si el cliente mayorista no existe en la base de datos.
        """

        user = await self.__user_repo.get_user(
            filters={
                "id": wholesaler_id,
                "role": UserRoles.CUSTOMER_WHOLESALE.value,
            },
            load_permissions=False,
        )

        if not user:
            raise ResourceNotFound()

        products, total_items = await self.__product_repo.get_products_by_wholesaler(
            products_id=user.customer_wholesale.products,
            offset=offset,
            limit=limit,
        )

        if not products:
            return [], 0

        result = []

        for product in products:
            dto = ReadProductPrivateDTO.model_construct(**product.to_dict())
            result.append(dto)

        return result, total_items
