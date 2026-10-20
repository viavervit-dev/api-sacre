from decimal import Decimal
from typing import Any
from uuid import UUID

from fastapi.exceptions import RequestValidationError
from pydantic import HttpUrl, TypeAdapter

from src.api.common.constants import TAX_PERCENTAGE
from src.api.common.exceptions import ResourceNotFound
from src.api.modules.inventory.constants import ProductEntity
from src.api.modules.inventory.dto import ReadProductPrivateDTO, UpdateProductPublicDTO
from src.api.modules.inventory.models.product import Product
from src.api.modules.inventory.repositories.interfaces import (
    ICategoryRepository,
    IProductRepository,
)
from src.api.modules.inventory.services.products.utils import ProductPricingMixin


class UpdateProductService(ProductPricingMixin):
    """Servicio encargado de la actualización de productos."""

    def __init__(
        self,
        product_repo: IProductRepository,
        category_repo: ICategoryRepository,
    ) -> None:
        self.__product_repo = product_repo
        self.__category_repo = category_repo

    async def update(
        self,
        data: UpdateProductPublicDTO,
        product_id: UUID,
    ) -> ReadProductPrivateDTO:
        """
        Actualiza un producto aplicando validaciones de negocio y recálculo de precios.

        Raises:
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
            ResourceNotFound: Si el producto no existe en la base de datos.
        """

        product_data = data.model_dump(exclude_unset=True)
        product = await self.__product_repo.get_product_by_id(id=product_id)

        if not product:
            raise ResourceNotFound()

        await self.__run_business_validations(data=product_data, instance=product)
        stock_total: int | None = product_data.get("stock_total")

        if stock_total and stock_total == 0 and product.stock_hand == 0:
            product_data["status"] = False

        # Calcular el precio de venta
        price_neto: Decimal | None = product_data.get("price_neto")
        profit_margin: Decimal | None = product_data.get("profit_margin")
        product_data["price_sale"] = self._calculate_sale_price(
            price_neto=price_neto or product.price_neto,
            profit_margin=profit_margin or product.profit_margin,
            iva=TAX_PERCENTAGE,
        )

        # Calcular el monto del IVA
        product_data["tax_amount"] = self._calculate_tax_amount(
            price_sale=product_data["price_sale"],
            iva=TAX_PERCENTAGE,
        )

        # Actualizar el producto en la base de datos
        updated_product = await self.__product_repo.update_product(
            data=product_data,
            instance=product,
        )

        return ReadProductPrivateDTO.model_construct(**updated_product.to_dict())

    async def __run_business_validations(self, data: dict[str, Any], instance: Product) -> None:
        """
        Ejecuta las validaciones de negocio previas a la actualización del producto.

        Raises:
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        errors = []

        # Validar que el stock_total no sea menor al stock_hand
        if data.get("stock_total"):
            stock_total: int | None = data.get("stock_total")

            if stock_total and stock_total < instance.stock_hand:
                errors.append(
                    {
                        "loc": ("body", "stock_total"),
                        "msg": ProductEntity.STOCK_TOTAL_INVALID.value,
                        "type": "domain_validation",
                    }
                )

        # Validar que el nombre del producto no esté registrado en la base de datos
        if data.get("name"):
            exists = await self.__product_repo.exists_product(filters={"name": data["name"]})

            if exists:
                errors.append(
                    {
                        "loc": ("body", "name"),
                        "msg": ProductEntity.NAME_IN_USE.value,
                        "type": "domain_validation",
                    }
                )

        # Validar que cada elemento de la lista de imágenes sea una URL válida
        if data.get("images"):
            adapter = TypeAdapter(HttpUrl)

            for i, url in enumerate(data["images"]):
                try:
                    adapter.validate_python(url)
                except Exception:
                    errors.append(
                        {
                            "loc": ("body", "images", i),  # type: ignore
                            "msg": ProductEntity.URL_INVALID.value,
                            "type": "domain_validation",
                        }
                    )

        # Validar que cada categoría exista en la base de datos
        if data.get("categories"):
            for i, category in enumerate(data["categories"]):
                exists = await self.__category_repo.exists_category(filters={"name": category})

                if not exists:
                    errors.append(
                        {
                            "loc": ("body", "categories", i),  # type: ignore
                            "msg": ProductEntity.CATEGORY_NOT_FOUND.value,
                            "type": "domain_validation",
                        }
                    )

        if errors:
            raise RequestValidationError(errors=errors)
