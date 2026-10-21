from uuid import UUID

from src.api.common.exceptions import DomainRuleViolation, ResourceNotFound
from src.api.modules.inventory.constants import ExceptionErrorMessages
from src.api.modules.inventory.models.product import Product
from src.api.modules.inventory.repositories.interfaces import IProductRepository


class DeleteProductService:
    """Servicio encargado de la eliminación de productos."""

    def __init__(self, product_repo: IProductRepository) -> None:
        self.__product_repo = product_repo

    async def delete(self, product_id: UUID) -> None:
        """
        Elimina un producto tras validar las reglas de negocio del dominio.

        Raises:
            DomainRuleViolation: Si falla alguna validación de las reglas de negocio.
        """

        # Validar que el producto exista en la base de datos
        product = await self.__product_repo.get_product_by_id(id=product_id)

        if not product:
            raise ResourceNotFound()

        # Ejecutamos validaciones de las reglas de negocio
        await self.__run_business_validations(instance=product)

        await self.__product_repo.delete_product(instance=product)

    async def __run_business_validations(self, instance: Product) -> None:
        """
        Valida que el producto cumpla las condiciones requeridas para su eliminación.

        Raises:
            DomainRuleViolation: Si falla alguna validación de las reglas de negocio.
        """

        if instance.stock_hand > 0:
            raise DomainRuleViolation(
                message=ExceptionErrorMessages.PRODUCT_HAS_RESERVED_STOCK.value
            )
