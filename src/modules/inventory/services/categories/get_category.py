from src.modules.inventory.dto import PrivateReadCategoryDTO, PublicReadCategoryDTO
from src.modules.inventory.repositories.interfaces import ICategoryRepository


class RetrieveCategoryService:
    """Servicio encargado de la consulta y serialización de categorías de productos."""

    def __init__(self, category_repo: ICategoryRepository) -> None:
        self.__category_repo = category_repo

    async def get_list_categories(
        self,
        private: bool,
        offset: int,
        limit: int,
        status: bool | None = None,
    ) -> tuple[list[PrivateReadCategoryDTO | PublicReadCategoryDTO], int]:
        """Obtiene una lista paginada de categorías según filtros y nivel de visibilidad."""

        categories, total_items = await self.__category_repo.get_list_categories(
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
