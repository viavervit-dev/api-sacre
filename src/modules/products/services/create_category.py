from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.products.dto import CreateCategoryDTO, PrivateReadCategoryDTO
from src.modules.products.repositories.interfaces import IProductRepository


class CreateCategoryService:
    """Servicio para la creación de categorías de productos en la base de datos."""

    def __init__(self, product_repo: type[IProductRepository], db: AsyncSession) -> None:
        self.__product_repo = product_repo
        self.__db = db

    async def create_category(self, data: CreateCategoryDTO) -> PrivateReadCategoryDTO:
        """Crea una nueva categoría de productos en la base de datos."""

        category_data = data.model_dump()
        category_data["status"] = False  # Asignar estado activo por defecto
        category_data["product_count"] = 0  # Asignar contador de productos por defecto
        category_instance = await self.__product_repo.create_category(
            db=self.__db,
            data=category_data,
        )
        category = PrivateReadCategoryDTO.model_construct(
            id=category_instance.id,
            name=category_instance.name,
            description=category_instance.description,
            product_count=category_instance.product_count,
            status=category_instance.status,
        )

        return category
