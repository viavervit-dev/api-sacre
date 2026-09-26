from uuid import UUID

from src.common.exceptions import DomainRuleViolation, ResourceNotFound
from src.modules.inventory.constants import ExceptionErrorMessages
from src.modules.inventory.models.product import Product
from src.modules.inventory.repositories.interfaces import IProductRepository


class DeleteProductService:
    """Servicio encargado de la validación de negocio y eliminación de productos."""

    def __init__(self, product_repo: IProductRepository) -> None:
        self.__product_repo = product_repo

    async def delete_product(self, product_id: UUID) -> None:
        """
        Elimina un producto tras validar las reglas de negocio del dominio.

        Raises:
            DomainRuleViolation: Si el producto tiene stock reservado en mano.
            ResourceNotFound: Si el producto no existe en la base de datos.
        """

        instance = await self.__product_repo.get_product(id=product_id)

        if not instance:
            raise ResourceNotFound()

        await self.__run_business_validations(instance=instance)
        await self.__product_repo.delete_product(instance=instance)

    async def __run_business_validations(self, instance: Product) -> None:
        """
        Valida que el producto cumpla las condiciones requeridas para su eliminación.

        Raises:
            DomainRuleViolation: Si el producto posee stock reservado (stock_hand > 0).
        """

        if instance.stock_hand > 0:
            raise DomainRuleViolation(
                message=ExceptionErrorMessages.PRODUCT_HAS_RESERVED_STOCK.value
            )
