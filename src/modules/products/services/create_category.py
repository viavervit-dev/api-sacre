from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.products.dto import CreateCategoryDTO, ReadCategoryDTO
from src.modules.products.repositories.interfaces import IProductRepository


class CreateCategoryService:
    """Servicio para la creación de categorías de productos en la base de datos."""

    def __init__(self, product_repo: type[IProductRepository], db: AsyncSession) -> None:
        self.__product_repo = product_repo
        self.__db = db

    async def create_category(self, data: CreateCategoryDTO) -> ReadCategoryDTO:
        """Crea una nueva categoría de productos en la base de datos."""

        category_data = data.model_dump()
        category_data["status"] = False  # Asignar estado activo por defecto
        category_data["product_count"] = 0  # Asignar contador de productos por defecto
        categpry_instance = await self.__product_repo.create_category(
            db=self.__db,
            data=category_data,
        )
        category = ReadCategoryDTO.model_construct(
            id=categpry_instance.id,
            name=categpry_instance.name,
            description=categpry_instance.description,
            product_count=categpry_instance.product_count,
            status=categpry_instance.status,
        )

        return category
