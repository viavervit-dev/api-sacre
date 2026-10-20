from collections.abc import Sequence

from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.models.user import User
from src.api.modules.inventory.dto import ReadProductPrivateDTO, ReadProductPublicDTO
from src.api.modules.inventory.repositories.interfaces import IProductRepository


class GetListProductsService:
    """Servicio encargado de la consulta y serialización de productos."""

    def __init__(self, product_repo: IProductRepository) -> None:
        self.__product_repo = product_repo

    async def get_list(
        self,
        user: User | None,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[ReadProductPublicDTO | ReadProductPrivateDTO], int]:
        """Obtiene una lista paginada de productos según filtros y nivel de visibilidad."""

        if user and user.role == UserRoles.ADMINISTRATOR.value:
            return await self.__get_products_private_catalog(
                offset=offset,
                limit=limit,
            )

        # Tanto clientes autenticados como usuarios anónimos ven el catálogo público
        return await self.__get_products_public_catalog(
            offset=offset,
            limit=limit,
        )

    async def __get_products_public_catalog(
        self,
        offset: int,
        limit: int,
    ) -> tuple[list[ReadProductPublicDTO], int]:
        """Consulta y serializa los productos correspondientes del catálogo público."""

        result = []

        products, total_items = await self.__product_repo.get_products_public_catalog(
            offset=offset,
            limit=limit,
        )

        if not products:
            return [], 0

        for product in products:
            dto = ReadProductPublicDTO.model_construct(**product.to_dict())
            result.append(dto)

        return result, total_items

    async def __get_products_private_catalog(
        self,
        offset: int,
        limit: int,
    ) -> tuple[list[ReadProductPrivateDTO], int]:
        """Consulta y serializa los productos correspondientes del catálogo privado."""

        result = []

        products, total_items = await self.__product_repo.get_products_private_catalog(
            offset=offset,
            limit=limit,
        )

        if not products:
            return [], 0

        for product in products:
            dto = ReadProductPrivateDTO.model_construct(**product.to_dict())
            result.append(dto)

        return result, total_items
