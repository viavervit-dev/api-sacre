from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.inventory.dto import PrivateReadCategoryDTO, PublicReadCategoryDTO
from src.modules.inventory.repositories.interfaces import IProductRepository


class GetCategoryService:
    """Servicio para la obtención de categorías de productos en la base de datos."""

    def __init__(self, product_repo: type[IProductRepository], db: AsyncSession) -> None:
        self.__product_repo = product_repo
        self.__db = db

    async def get_list_categories(
        self,
        private: bool,
        offset: int,
        limit: int,
        status: bool | None = None,
    ) -> tuple[list[PrivateReadCategoryDTO | PublicReadCategoryDTO], int]:
        """Obtiene una lista de categorías de productos según su estado."""

        categories, total_items = await self.__product_repo.get_list_categories(
            db=self.__db,
            status=status,
            offset=offset,
            limit=limit,
        )

        if not categories:
            return [], 0

        result = []

        for category in categories:
            if private:
                dto = PrivateReadCategoryDTO.model_construct(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    product_count=category.product_count,
                    status=category.status,
                )
            else:
                dto = PublicReadCategoryDTO.model_construct(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    product_count=category.product_count,
                )

            result.append(dto)

        return result, total_items
