from uuid import UUID

from src.modules.inventory.dto import PrivateReadProductDTO
from src.modules.inventory.repositories.interfaces import IProductRepository


class RetrieveProductsWholesalerService:
    """Servicio encargado de la consulta y serialización de productos de un mayorista."""

    def __init__(self, product_repo: IProductRepository) -> None:
        self.__product_repo = product_repo

    async def get_products_by_wholesaler(
        self,
        wholesaler_id: UUID,
        offset: int,
        limit: int,
    ) -> tuple[list[PrivateReadProductDTO], int]:
        """Obtiene una lista paginada de los productos exclusivos de un cliente mayorista."""

        products, total_items = await self.__product_repo.get_products_by_wholesaler(
            wholesaler_id=wholesaler_id,
            offset=offset,
            limit=limit,
        )

        if not products:
            return [], 0

        result = []

        for product in products:
            dto = PrivateReadProductDTO.model_construct(
                id=product.id,
                name=product.name,
                categories=product.categories,
                description_short=product.description_short,
                description_long=product.description_long,
                images=product.images,
                price_neto=product.price_neto,
                price_sale=product.price_sale,
                profit_margin=product.profit_margin,
                iva=product.iva,
                stock_total=product.stock_total,
                stock_hand=product.stock_hand,
                stock_sale=product.stock_sale,
                status=product.status,
            )
            result.append(dto)

        return result, total_items
