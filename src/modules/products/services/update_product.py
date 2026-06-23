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
        instance: Product,
    ) -> PrivateReadProductDTO:
        """Actualiza los datos de un producto en la base de datos."""

        product_data = data.model_dump(exclude_unset=True)

        # Validaciones de stock_total en relación a stock_hand
        stock_total: int | None = product_data.get("stock_total", None)

        if stock_total and stock_total < instance.stock_hand:
            raise RequestValidationError(
                errors=[
                    {
                        "loc": ("body", "stock_total"),
                        "msg": ProductEntity.STOCK_TOTAL_INVALID.value,
                        "type": "domain_validation",
                    }
                ]
            )
        if stock_total and stock_total == 0 and instance.stock_hand == 0:
            product_data["status"] = False

        # Calcular el precio de venta
        price_neto: Decimal | None = product_data.get("price_neto", None)
        profit_margin: Decimal | None = product_data.get("profit_margin", None)
        iva: VatRatesProduct | None = product_data.get("iva", None)
        product_data["price_sale"] = self._calculate_sale_price(
            price_neto=price_neto or instance.price_neto,
            iva=iva.value if iva else instance.iva,
            profit_margin=profit_margin or instance.profit_margin,
        )

        # Actualizar el producto en la base de datos
        instance = await self.__product_repo.update_product(
            update_data=product_data,
            instance=instance,
            db=self.__db,
        )
        product = PrivateReadProductDTO.model_construct(
            id=instance.id,
            name=instance.name,
            categories=instance.categories,
            description_short=instance.description_short,
            description_long=instance.description_long,
            images=instance.images,
            price_neto=instance.price_neto,
            price_sale=instance.price_sale,
            profit_margin=instance.profit_margin,
            iva=instance.iva,
            stock_total=instance.stock_total,
            stock_hand=instance.stock_hand,
            stock_sale=instance.stock_sale,
            status=instance.status,
        )

        return product
