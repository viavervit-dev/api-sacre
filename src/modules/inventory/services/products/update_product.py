from decimal import Decimal
from typing import Any
from uuid import UUID

from fastapi.exceptions import RequestValidationError
from pydantic import HttpUrl, TypeAdapter

from src.common.exceptions import ResourceNotFound
from src.modules.inventory.constants import ProductEntity, VatRatesProduct
from src.modules.inventory.dto import PrivateReadProductDTO, UpdateProductDTO
from src.modules.inventory.models.product import Product
from src.modules.inventory.repositories.interfaces import ICategoryRepository, IProductRepository
from src.modules.inventory.services.products.utils import ProductPricingMixin


class UpdateProductService(ProductPricingMixin):
    """Servicio para la validación de negocio y actualización de productos."""

    def __init__(
        self,
        product_repo: IProductRepository,
        category_repo: ICategoryRepository,
    ) -> None:
        self.__product_repo = product_repo
        self.__category_repo = category_repo

    async def update_product(
        self,
        data: UpdateProductDTO,
        product_id: UUID,
    ) -> PrivateReadProductDTO:
        """
        Actualiza un producto aplicando validaciones de negocio y recálculo de precios.

        Raises:
            RequestValidationError: Si falla alguna validacion de negocio.
            ResourceNotFound: Si el producto no existe en la base de datos.
        """

        product_data = data.model_dump(exclude_unset=True)
        instance = await self.__product_repo.get_product(id=product_id)

        if not instance:
            raise ResourceNotFound()

        await self.__run_business_validations(product_data=product_data, instance=instance)
        stock_total: int | None = product_data.get("stock_total")

        if stock_total and stock_total == 0 and instance.stock_hand == 0:
            product_data["status"] = False

        # Calcular el precio de venta
        price_neto: Decimal | None = product_data.get("price_neto")
        profit_margin: Decimal | None = product_data.get("profit_margin")
        iva: VatRatesProduct | None = product_data.get("iva")
        product_data["price_sale"] = self._calculate_sale_price(
            price_neto=price_neto or instance.price_neto,
            iva=iva.value if iva else instance.iva,
            profit_margin=profit_margin or instance.profit_margin,
        )

        # Actualizar el producto en la base de datos
        instance = await self.__product_repo.update_product(
            update_data=product_data,
            instance=instance,
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

    async def __run_business_validations(
        self,
        product_data: dict[str, Any],
        instance: Product,
    ) -> None:
        """
        Ejecuta las validaciones de negocio previas a la actualización del producto.

        Raises:
            RequestValidationError: Si falla alguna validacion de negocio.
        """

        errors = []

        # Validar que el stock_total no sea menor al stock_hand
        if product_data.get("stock_total"):
            stock_total: int | None = product_data.get("stock_total")

            if stock_total and stock_total < instance.stock_hand:
                errors.append(
                    {
                        "loc": ("body", "stock_total"),
                        "msg": ProductEntity.STOCK_TOTAL_INVALID.value,
                        "type": "domain_validation",
                    }
                )

        # Validar que el nombre del producto no esté registrado en la base de datos
        if product_data.get("name"):
            exists = await self.__product_repo.exists_product(
                filters={"name": product_data["name"]}
            )

            if exists:
                errors.append(
                    {
                        "loc": ("body", "name"),
                        "msg": ProductEntity.NAME_IN_USE.value,
                        "type": "domain_validation",
                    }
                )

        # Validar que cada elemento de la lista de imágenes sea una URL válida
        if product_data.get("images"):
            adapter = TypeAdapter(HttpUrl)

            for i, url in enumerate(product_data["images"]):
                try:
                    adapter.validate_python(url)
                except Exception:
                    errors.append(
                        {
                            "loc": ("body", "images", i),
                            "msg": ProductEntity.URL_INVALID.value,
                            "type": "domain_validation",
                        }
                    )

        # Validar que cada categoría exista en la base de datos
        if product_data.get("categories"):
            for i, category in enumerate(product_data["categories"]):
                exists = await self.__category_repo.exists_category(filters={"name": category})

                if not exists:
                    errors.append(
                        {
                            "loc": ("body", "categories", i),
                            "msg": ProductEntity.CATEGORY_NOT_FOUND.value,
                            "type": "domain_validation",
                        }
                    )

        if errors:
            raise RequestValidationError(errors=errors)
