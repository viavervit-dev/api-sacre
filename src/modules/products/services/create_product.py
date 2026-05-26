from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.products.dto import CreateProductDTO, ReadProductDTO
from src.modules.products.repositories.interfaces import IProductRepository


class CreateProductService:
    """Servicio para la creación de productos en la base de datos."""

    def __init__(self, product_repo: type[IProductRepository], session: AsyncSession) -> None:
        self.__product_repo = product_repo
        self.__session = session

    async def create_product(self, data: CreateProductDTO) -> ReadProductDTO:
        """Crea un nuevo producto en la base de datos."""

        product_data = data.model_dump()

        if product_data["stock_total"] > 0:
            product_data["status"] = True  # Asignar estado activo por defecto
        else:
            product_data["status"] = False  # Asignar estado inactivo por defecto

        product_instance = await self.__product_repo.create_product(
            session=self.__session,
            data=product_data,
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
