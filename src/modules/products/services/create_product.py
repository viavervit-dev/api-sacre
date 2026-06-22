from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.products.constants import VatRatesProduct
from src.modules.products.dto import CreateProductDTO, PrivateReadProductDTO
from src.modules.products.repositories.interfaces import IProductRepository
from src.modules.products.services.utils import ProductServiceBase


class CreateProductService(ProductServiceBase):
    """Servicio para la creación de productos en la base de datos."""

    def __init__(self, product_repo: type[IProductRepository], db: AsyncSession) -> None:
        self.__product_repo = product_repo
        self.__db = db

    async def create_product(self, data: CreateProductDTO) -> PrivateReadProductDTO:
        """Crea un nuevo producto en la base de datos."""

        product_data = data.model_dump()
        iva: VatRatesProduct = product_data["iva"]
        product_data["iva"] = iva.value

        # Asignar el estado del producto según el stock total
        if product_data["stock_total"] > 0:
            product_data["status"] = True
        else:
            product_data["status"] = False

        # Incrementar el contador de productos asociados a cada categoría
        for category in product_data["categories"]:
            await self.__product_repo.add_product_to_category(db=self.__db, name=category)

        # Calcular el precio de venta
        product_data["price_sale"] = self._calculate_sale_price(
            price_neto=product_data["price_neto"],
            profit_margin=product_data["profit_margin"],
            iva=product_data["iva"],
        )

        # Inicializar el stock en mano y el stock de venta en 0
        product_data["stock_hand"] = 0
        product_data["stock_sale"] = 0

        instance = await self.__product_repo.create_product(
            data=product_data,
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
