from typing import Any

from fastapi.exceptions import RequestValidationError
from pydantic import HttpUrl, TypeAdapter

from src.modules.inventory.constants import ProductEntity, VatRatesProduct
from src.modules.inventory.dto import CreateProductDTO, PrivateReadProductDTO
from src.modules.inventory.repositories.interfaces import ICategoryRepository, IProductRepository
from src.modules.inventory.services.products.utils import ProductPricingMixin


class CreateProductService(ProductPricingMixin):
    """Servicio para la validación de negocio, cálculo de precios y creación de productos."""

    def __init__(
        self,
        product_repo: IProductRepository,
        category_repo: ICategoryRepository,
    ) -> None:
        self.__product_repo = product_repo
        self.__category_repo = category_repo

    async def create_product(self, data: CreateProductDTO) -> PrivateReadProductDTO:
        """
        Crea un nuevo producto aplicando reglas de negocio, stock y cálculo de precios.

        Raises:
            RequestValidationError: Si falla alguna validacion de negocio.
        """

        product_data = data.model_dump()
        await self.__run_business_validations(product_data=product_data)
        iva: VatRatesProduct = product_data["iva"]
        product_data["iva"] = iva.value

        # Asignar el estado del producto según el stock total
        if product_data["stock_total"] > 0:
            product_data["status"] = True
        else:
            product_data["status"] = False

        # Incrementar el contador de productos asociados a cada categoría
        for category in product_data["categories"]:
            await self.__category_repo.add_product_to_category(name=category)

        # Calcular el precio de venta
        product_data["price_sale"] = self._calculate_sale_price(
            price_neto=product_data["price_neto"],
            profit_margin=product_data["profit_margin"],
            iva=product_data["iva"],
        )

        # Inicializar el stock en mano y el stock de venta en 0
        product_data["stock_hand"] = 0
        product_data["stock_sale"] = 0

        instance = await self.__product_repo.create_product(data=product_data)
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

    async def __run_business_validations(self, product_data: dict[str, Any]) -> None:
        """
        Ejecuta las validaciones de negocio previas a la creación del producto.

        Raises:
            RequestValidationError: Si falla alguna validacion de negocio.
        """

        errors = []

        # Validar que el nombre del producto no esté registrado en la base de datos
        exists = await self.__product_repo.exists_product(filters={"name": product_data["name"]})

        if exists:
            errors.append(
                {
                    "loc": ("body", "name"),
                    "msg": ProductEntity.NAME_IN_USE.value,
                    "type": "domain_validation",
                }
            )

        # Validar que cada elemento de la lista de imágenes sea una URL válida
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
