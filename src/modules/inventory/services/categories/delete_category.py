from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions import DomainRuleViolation
from src.modules.inventory.constants import ExceptionErrorMessages
from src.modules.inventory.models.category import Category
from src.modules.inventory.repositories.interfaces import IProductRepository


class DeleteCategoryService:
    """Servicio para eliminar una categoría de productos en la base de datos."""

    def __init__(self, product_repo: type[IProductRepository], db: AsyncSession) -> None:
        self.__product_repo = product_repo
        self.__db = db

    async def delete_category(self, instance: Category) -> None:
        """Elimina una categoría de productos de la base de datos."""

        if instance.product_count > 0:
            raise DomainRuleViolation(
                message=ExceptionErrorMessages.CATEGORY_HAS_DEPENDENCIES.value
            )

        await self.__product_repo.delete_category(instance=instance, db=self.__db)
