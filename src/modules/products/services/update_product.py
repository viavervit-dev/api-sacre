from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.constants import TWO_DECIMAL_PLACES
from src.common.exceptions import ResourceNotFound
from src.modules.products.constants import ProductEntity, VatRatesProduct
from src.modules.products.dto import ReadProductDTO, UpdateProductDTO
from src.modules.products.repositories.interfaces import IProductRepository


class UpdateProductService:
    """Servicio para la actualización de productos en la base de datos."""

    def __init__(self, product_repo: type[IProductRepository], db: AsyncSession) -> None:
        self.__product_repo = product_repo
        self.__db = db

    async def update_product(self, data: UpdateProductDTO, id: UUID) -> ReadProductDTO:
        """Actualiza los datos de un producto en la base de datos."""

        if not await self.__product_repo.exists_product(db=self.__db, filters={"id": id}):
            raise ResourceNotFound()

        product_data = data.model_dump()
        price_neto: Decimal | None = product_data.get("price_neto", None)
        iva: VatRatesProduct | None = product_data.get("iva", None)
        stock_total: int | None = product_data.get("stock_total", None)

        product_instance = await self.__product_repo.get_product_by_id(db=self.__db, id=id)

        # Validar que el stock total no sea menor al stock en reserva
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

        # Actualizar el estado del producto si se requiere
        if stock_total and stock_total == 0 and product_instance.stock_hand == 0:
            product_data["status"] = False

        # Calcular el precio de venta a partir del precio neto e IVA
        if iva and not price_neto:
            product_data["iva"] = iva.value
            raw_price_sale = product_instance.price_neto * (Decimal("1.0000") + iva.value)
            product_data["price_sale"] = raw_price_sale.quantize(
                exp=TWO_DECIMAL_PLACES,
                rounding=ROUND_HALF_UP,
            )
        if price_neto and not iva:
            raw_price_sale = price_neto * (Decimal("1.0000") + product_instance.iva)
            product_data["price_sale"] = raw_price_sale.quantize(
                exp=TWO_DECIMAL_PLACES,
                rounding=ROUND_HALF_UP,
            )
        if price_neto and iva:
            product_data["iva"] = iva.value
            raw_price_sale = price_neto * (Decimal("1.0000") + iva.value)
            product_data["price_sale"] = raw_price_sale.quantize(
                exp=TWO_DECIMAL_PLACES,
                rounding=ROUND_HALF_UP,
            )

        product_instance = await self.__product_repo.update_product(
            update_data=product_data,
            db=self.__db,
            id=id,
        )
        product = ReadProductDTO.model_construct(
            id=product_instance.id,
            name=product_instance.name,
            categories=product_instance.categories,
            description_short=product_instance.description_short,
            description_long=product_instance.description_long,
            images=product_instance.images,
            price_neto=product_instance.price_neto,
            price_sale=product_instance.price_sale,
            iva=product_instance.iva,
            stock_total=product_instance.stock_total,
            stock_hand=product_instance.stock_hand,
            stock_sale=product_instance.stock_sale,
            status=product_instance.status,
        )

        return product
