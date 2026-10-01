from typing import Any
from uuid import UUID

from fastapi.exceptions import RequestValidationError
from pydantic import HttpUrl, TypeAdapter

from src.common.exceptions import ResourceNotFound
from src.modules.inventory.constants import ProductEntity, VatRatesProduct
from src.modules.inventory.dto import CreateProductDTO, ReadProductWholesalerDTO
from src.modules.inventory.repositories.interfaces import ICategoryRepository, IProductRepository
from src.modules.inventory.services.products.utils import ProductPricingMixin
from src.modules.users.repositories.interfaces import ICustomerWholesaleRepository


class AddProductWholesaleService(ProductPricingMixin):
    """Servicio para la validación y creación de productos exclusivos para mayoristas."""

    def __init__(
        self,
        customer_wholesale_repo: ICustomerWholesaleRepository,
        product_repo: IProductRepository,
        category_repo: ICategoryRepository,
    ) -> None:
        self.__customer_wholesale_repo = customer_wholesale_repo
        self.__product_repo = product_repo
        self.__category_repo = category_repo

    async def add_product(
        self,
        data: CreateProductDTO,
        wholesaler_id: UUID,
    ) -> ReadProductWholesalerDTO:
        """
        Crea un producto exclusivo asignado a un cliente mayorista.

        Raises:
            ResourceNotFound: Si el cliente mayorista no existe en la base de datos.
            RequestValidationError: Si alguna regla de validación de negocio falla.
        """

        # Validar que el cliente mayorista exista en la base de datos
        wholesale_instance = await self.__customer_wholesale_repo.get_wholesale(id=wholesaler_id)

        if not wholesale_instance:
            raise ResourceNotFound()

        # Validaciones de negocio
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

        # Inicializar el stock en mano y el stock de venta
        product_data["stock_hand"] = 0
        product_data["stock_sale"] = product_data["stock_total"]

        # Asignar la llave foránea al diccionario
        product_data["wholesaler_id"] = wholesaler_id

        product_instance = await self.__product_repo.create_product(data=product_data)

        return ReadProductWholesalerDTO.model_construct(
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
            wholesaler_id=product_instance.wholesaler_id,
        )

    async def __run_business_validations(self, product_data: dict[str, Any]) -> None:
        """
        Ejecuta las validaciones de negocio previas al registro del producto.

        Raises:
            RequestValidationError: Si falla alguna regla de validación de negocio.
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
