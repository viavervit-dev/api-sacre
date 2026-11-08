from uuid import UUID

from src.api.common.exceptions import ResourceNotFound
from src.api.modules.inventory.repositories.interfaces import IWholesalerProductRepository


class DeleteProductWholesalerService:
    """Servicio encargado de la eliminación de productos de clientes mayoristas."""

    def __init__(self, wholesaler_product_repo: IWholesalerProductRepository) -> None:
        self.__wholesaler_product_repo = wholesaler_product_repo

    async def delete(self, product_id: UUID) -> None:
        """
        Elimina un producto de un cliente mayorista.

        Raises:
            ResourceNotFound: Si el producto no existe en la base de datos.
        """

        # Validar que el producto exista en la base de datos
        product = await self.__wholesaler_product_repo.get_product_by_id(id=product_id)

        if not product:
            raise ResourceNotFound()

        await self.__wholesaler_product_repo.delete_product(instance=product)
