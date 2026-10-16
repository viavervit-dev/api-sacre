from collections.abc import Sequence

from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.models.user import User
from src.api.modules.inventory.dto import ReadCategoryPrivateDTO, ReadCategoryPublicDTO
from src.api.modules.inventory.repositories.interfaces import ICategoryRepository


class GetListCategoryService:
    """Servicio encargado de la consulta y serialización de categorías de productos."""

    def __init__(self, category_repo: ICategoryRepository) -> None:
        self.__category_repo = category_repo

    async def get_list_categories(
        self,
        user: User | None,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[ReadCategoryPrivateDTO | ReadCategoryPublicDTO], int]:
        """Obtiene una lista paginada de categorías según filtros y nivel de visibilidad."""

        if user and user.role == UserRoles.ADMINISTRATOR.value:
            return await self.__get_private_data_category(
                offset=offset,
                limit=limit,
            )

        # Tanto clientes autenticados como usuarios anónimos ven los datos público
        return await self.__get_public_data_category(
            offset=offset,
            limit=limit,
        )

    async def __get_public_data_category(
        self,
        offset: int,
        limit: int,
    ) -> tuple[list[ReadCategoryPublicDTO], int]:
        """
        Consulta y serializa los datos públicos de las categorías de productos correspondientes.
        """

        result = []

        categories, total_items = await self.__category_repo.get_list_categories_activated(
            offset=offset,
            limit=limit,
        )

        if not categories:
            return [], 0

        for category in categories:
            dto = ReadCategoryPublicDTO.model_construct(
                id=category.id,
                name=category.name,
                description=category.description,
            )
            result.append(dto)

        return result, total_items

    async def __get_private_data_category(
        self,
        offset: int,
        limit: int,
    ) -> tuple[list[ReadCategoryPrivateDTO], int]:
        """
        Consulta y serializa los datos públicos y privados de las categorías de productos
        correspondientes.
        """

        result = []

        categories, total_items = await self.__category_repo.get_list_categories(
            offset=offset,
            limit=limit,
        )

        if not categories:
            return [], 0

        for category in categories:
            dto = ReadCategoryPrivateDTO.model_construct(
                id=category.id,
                name=category.name,
                description=category.description,
                status=category.status,
            )
            result.append(dto)

        return result, total_items
