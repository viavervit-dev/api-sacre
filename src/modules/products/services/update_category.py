from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.products.dto import ReadCategoryDTO, UpdateCategoryDTO
from src.modules.products.models.category import Category
from src.modules.products.repositories.interfaces import IProductRepository


class UpdateCategoryService:
    """Servicio para la actualización de una categoria de producto en la base de datos."""

    def __init__(self, product_repo: type[IProductRepository], db: AsyncSession) -> None:
        self.__product_repo = product_repo
        self.__db = db

    async def update_category(
        self,
        data: UpdateCategoryDTO,
        category_instance: Category,
    ) -> ReadCategoryDTO:
        """Actualiza los datos de una categoria de producto en la base de datos."""

        category_data = data.model_dump()

        # Actualizar el producto en la base de datos
        category_instance = await self.__product_repo.update_category(
            update_data=category_data,
            id=category_instance.id,
            db=self.__db,
        )
        category = ReadCategoryDTO.model_construct(
            id=category_instance.id,
            name=category_instance.name,
            description=category_instance.description,
        )

        return category
