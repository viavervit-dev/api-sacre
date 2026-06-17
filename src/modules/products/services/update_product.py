from decimal import Decimal

from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.products.constants import ProductEntity, VatRatesProduct
from src.modules.products.dto import PrivateReadProductDTO, UpdateProductDTO
from src.modules.products.models.product import Product
from src.modules.products.repositories.interfaces import IProductRepository
from src.modules.products.services.utils import ProductServiceBase


class UpdateProductService(ProductServiceBase):
    """Servicio para la actualización de productos en la base de datos."""

    def __init__(self, product_repo: type[IProductRepository], db: AsyncSession) -> None:
        self.__product_repo = product_repo
        self.__db = db

    async def update_product(
        self,
        data: UpdateProductDTO,
        product_instance: Product,
    ) -> PrivateReadProductDTO:
        """Actualiza los datos de un producto en la base de datos."""

        product_data = data.model_dump()

        # Validaciones de stock_total en relación a stock_hand
        stock_total: int | None = product_data.get("stock_total", None)

        if stock_total and stock_total < product_instance.stock_hand:
            raise RequestValidationError(
                errors=[
                    {
                        "loc": ("body", "stock_total"),
                        "msg": ProductEntity.STOCK_TOTAL_INVALID.value,
                        "type": "domain_validation",
                    }
                ]
            )
        if stock_total and stock_total == 0 and product_instance.stock_hand == 0:
            product_data["status"] = False

        # Calcular el precio de venta
        price_neto: Decimal | None = product_data.get("price_neto", None)
        profit_margin: Decimal | None = product_data.get("profit_margin", None)
        iva: VatRatesProduct | None = product_data.get("iva", None)
        product_data["price_sale"] = self._calculate_sale_price(
            price_neto=price_neto or product_instance.price_neto,
            iva=iva.value if iva else product_instance.iva,
            profit_margin=profit_margin or product_instance.profit_margin,
        )

        # Actualizar el producto en la base de datos
        product_instance = await self.__product_repo.update_product(
            update_data=product_data,
            db=self.__db,
            id=product_instance.id,
        )
        product = PrivateReadProductDTO.model_construct(
            id=product_instance.id,
            name=product_instance.name,
            categories=product_instance.categories,
            description_short=product_instance.description_short,
            description_long=product_instance.description_long,
            images=product_instance.images,
            price_neto=product_instance.price_neto,
            price_sale=product_instance.price_sale,
            profit_margin=product_instance.profit_margin,
            iva=product_instance.iva,
            stock_total=product_instance.stock_total,
            stock_hand=product_instance.stock_hand,
            stock_sale=product_instance.stock_sale,
            status=product_instance.status,
        )

        return product
