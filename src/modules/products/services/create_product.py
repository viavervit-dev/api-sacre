from decimal import ROUND_HALF_UP, Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.constants import TWO_DECIMAL_PLACES
from src.modules.products.dto import CreateProductDTO, ReadProductDTO
from src.modules.products.repositories.interfaces import IProductRepository


class CreateProductService:
    """Servicio para la creación de productos en la base de datos."""

    def __init__(self, product_repo: type[IProductRepository], db: AsyncSession) -> None:
        self.__product_repo = product_repo
        self.__db = db

    async def create_product(self, data: CreateProductDTO) -> ReadProductDTO:
        """Crea un nuevo producto en la base de datos."""

        product_data = data.model_dump()

        # Asignar el estado del producto según el stock total
        if product_data["stock_total"] > 0:
            product_data["status"] = True
        else:
            product_data["status"] = False

        # Incrementar el contador de productos asociados a cada categoría
        for category in product_data["categories"]:
            await self.__product_repo.add_product_to_category(db=self.__db, name=category)

        # Calcular el precio de venta
        product_data["price_sale"] = self.__calculate_sale_price(
            price_neto=data.price_neto,
            iva=data.iva.value,
            profit_margin=data.profit_margin,
        )

        # Inicializar el stock en mano y el stock de venta en 0
        product_data["stock_hand"] = 0
        product_data["stock_sale"] = 0

        product_instance = await self.__product_repo.create_product(
            data=product_data,
            db=self.__db,
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
            profit_margin=product_instance.profit_margin,
            iva=product_instance.iva,
            stock_total=product_instance.stock_total,
            stock_hand=product_instance.stock_hand,
            stock_sale=product_instance.stock_sale,
            status=product_instance.status,
        )

        return product

    @staticmethod
    def __calculate_sale_price(
        price_neto: Decimal,
        iva: Decimal,
        profit_margin: Decimal,
    ) -> Decimal:
        """Calcula el precio de venta a partir del precio neto, IVA y margen de beneficio."""

        raw_price_sale = price_neto * (Decimal("1.0000") + profit_margin)
        raw_price_sale = raw_price_sale * (Decimal("1.0000") + iva)

        return raw_price_sale.quantize(
            exp=TWO_DECIMAL_PLACES,
            rounding=ROUND_HALF_UP,
        )
