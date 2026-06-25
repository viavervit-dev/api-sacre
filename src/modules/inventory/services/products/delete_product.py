from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions import DomainRuleViolation
from src.modules.inventory.models.product import Product
from src.modules.inventory.repositories.interfaces import IProductRepository


class DeleteProductService:
    """Servicio para eliminar productos en la base de datos."""

    def __init__(self, product_repo: type[IProductRepository], db: AsyncSession) -> None:
        self.__product_repo = product_repo
        self.__db = db

    async def delete_product(self, instance: Product) -> None:
        """Elimina un producto de la base de datos."""

        if instance.stock_hand > 0:
            raise DomainRuleViolation()

        await self.__product_repo.delete_product(instance=instance, db=self.__db)
