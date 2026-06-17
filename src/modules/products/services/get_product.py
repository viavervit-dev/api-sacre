from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.products.dto import PrivateReadProductDTO, PublicReadProductDTO
from src.modules.products.repositories.interfaces import IProductRepository


class GetProductService:
    """Servicio para la obtención de productos en la base de datos."""

    def __init__(self, product_repo: type[IProductRepository], db: AsyncSession) -> None:
        self.__product_repo = product_repo
        self.__db = db

    async def get_list_products(
        self,
        private: bool,
        offset: int,
        limit: int,
        status: bool | None = None,
    ) -> tuple[list[PrivateReadProductDTO | PublicReadProductDTO], int]:
        """Obtiene una lista de productos según su estado."""

        products, total_items = await self.__product_repo.get_list_products(
            db=self.__db,
            status=status,
            offset=offset,
            limit=limit,
        )

        if not products:
            return [], 0

        result = []

        for product in products:
            if private:
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
            else:
                dto = PublicReadProductDTO.model_construct(
                    id=product.id,
                    name=product.name,
                    categories=product.categories,
                    description_short=product.description_short,
                    description_long=product.description_long,
                    images=product.images,
                    price_sale=product.price_sale,
                    stock_sale=product.stock_sale,
                )

            result.append(dto)

        return result, total_items
