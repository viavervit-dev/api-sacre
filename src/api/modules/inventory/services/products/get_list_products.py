from collections.abc import Sequence

from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.models.user import User
from src.api.modules.inventory.dto import ReadProductPrivateDTO, ReadProductPublicDTO
from src.api.modules.inventory.repositories.interfaces import IProductRepository


class RetrieveListProductsService:
    """Servicio encargado de la consulta y serialización de productos."""

    def __init__(self, product_repo: IProductRepository) -> None:
        self.__product_repo = product_repo

    async def get_list_products(
        self,
        user: User | None,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[ReadProductPublicDTO | ReadProductPrivateDTO], int]:
        """Obtiene una lista paginada de productos según filtros y nivel de visibilidad."""

        if user and user.role == UserRoles.ADMINISTRATOR.value:
            return await self.__get_products_private_catalog(
                offset=offset,
                limit=limit,
            )

        # Tanto clientes autenticados como usuarios anónimos ven el catálogo público
        return await self.__get_products_public_catalog(
            offset=offset,
            limit=limit,
        )

    async def __get_products_public_catalog(
        self,
        offset: int,
        limit: int,
    ) -> tuple[list[ReadProductPublicDTO], int]:
        """Consulta y serializa los productos correspondientes del catálogo público."""

        result = []

        products, total_items = await self.__product_repo.get_products_public_catalog(
            offset=offset,
            limit=limit,
        )

        if not products:
            return [], 0

        for product in products:
            dto = ReadProductPublicDTO.model_construct(
                id=product.id,
                name=product.name,
                categories=product.categories,
                description_short=product.description_short,
                description_long=product.description_long,
                images=product.images,
                price_neto=product.price_neto,
                price_sale=product.price_sale,
                profit_margin=product.profit_margin,
                tax_amount=product.tax_amount,
                stock_total=product.stock_total,
                stock_hand=product.stock_hand,
                stock_sale=product.stock_sale,
                status=product.status,
            )
            result.append(dto)

        return result, total_items

    async def __get_products_private_catalog(
        self,
        offset: int,
        limit: int,
    ) -> tuple[list[ReadProductPrivateDTO], int]:
        """Consulta y serializa los productos correspondientes del catálogo privado."""

        result = []

        products, total_items = await self.__product_repo.get_products_private_catalog(
            offset=offset,
            limit=limit,
        )

        if not products:
            return [], 0

        for product in products:
            dto = ReadProductPrivateDTO.model_construct(
                id=product.id,
                name=product.name,
                categories=product.categories,
                description_short=product.description_short,
                description_long=product.description_long,
                images=product.images,
                price_neto=product.price_neto,
                price_sale=product.price_sale,
                profit_margin=product.profit_margin,
                tax_amount=product.tax_amount,
                stock_total=product.stock_total,
                stock_hand=product.stock_hand,
                stock_sale=product.stock_sale,
                status=product.status,
            )
            result.append(dto)

        return result, total_items
