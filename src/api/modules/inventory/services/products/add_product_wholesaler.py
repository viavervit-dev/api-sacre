from uuid import UUID

from fastapi.exceptions import RequestValidationError
from pydantic import HttpUrl, TypeAdapter

from src.api.common.exceptions import ResourceNotFound
from src.api.common.utils import FinancialCalculationsMixin
from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.repositories.interfaces import IUserRepository
from src.api.modules.inventory.constants import ProductEntity
from src.api.modules.inventory.dto import CreateProductWholesalerDTO, ReadProductPrivateDTO
from src.api.modules.inventory.models.product import Product
from src.api.modules.inventory.repositories.interfaces import (
    ICategoryRepository,
    IProductRepository,
)
from src.api.modules.users.repositories.interfaces import IWholesalerRepository


class AddProductWholesalerService(FinancialCalculationsMixin):
    """Servicio encargado de la creación de productos exclusivos para mayoristas."""

    def __init__(
        self,
        wholesaler_repo: IWholesalerRepository,
        user_repo: IUserRepository,
        product_repo: IProductRepository,
        category_repo: ICategoryRepository,
    ) -> None:
        self.__wholesaler_repo = wholesaler_repo
        self.__user_repo = user_repo
        self.__product_repo = product_repo
        self.__category_repo = category_repo

    async def add_product(
        self,
        data: CreateProductWholesalerDTO,
        wholesaler_id: UUID,
    ) -> ReadProductPrivateDTO:
        """
        Crea un producto exclusivo asignado a un cliente mayorista.

        Raises:
            ResourceNotFound: Si el cliente mayorista no existe en la base de datos.
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        # Validar que el cliente mayorista exista en la base de datos
        user = await self.__user_repo.get_user(
            filters={"id": wholesaler_id, "role": UserRoles.WHOLESALER.value},
            load_permissions=False,
        )

        if not user:
            raise ResourceNotFound()

        # Creamos el producto
        product = await self.__create_product(data=data)

        # Agregamos el nuevo producto a la lista de productos existente
        products_wholesale = user.wholesaler.products
        products_wholesale.append(product.id)
        _ = self.__wholesaler_repo.update_wholesaler(
            instance=user.wholesaler,
            data={"products": products_wholesale},
        )

        return ReadProductPrivateDTO.model_construct(**product.to_dict())

    async def __create_product(self, data: CreateProductWholesalerDTO) -> Product:
        """
        Crea un nuevo producto para el catálogo público.

        Raises:
            RequestValidationError: Si falla alguna validacion de negocio.
        """

        # Ejecutamos validaciones de las reglas de negocio
        await self.__run_business_validations(data=data)

        product_data = data.model_dump()

        # Calcular el precio de venta
        product_data["price_sale"] = self.calculate_sale_price_product(
            price_neto=product_data["price_neto"],
            profit_margin=product_data["profit_margin"],
        )

        # Calcular el monto del IVA
        product_data["tax_amount"] = self.calculate_tax_amount(amount=product_data["price_sale"])

        # Inicializar algunos valores por defecto
        product_data["stock_sale"] = product_data["stock_total"]
        product_data["status"] = True
        product_data["exclusive"] = True
        product_data["stock_hand"] = 0

        return await self.__product_repo.create_product(data=product_data)

    async def __run_business_validations(self, data: CreateProductWholesalerDTO) -> None:
        """
        Ejecuta las validaciones de negocio previas al registro del producto.

        Raises:s
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        errors = []

        # Validar que el nombre del producto no esté registrado en la base de datos
        if data.name:
            exists = await self.__product_repo.exists_product(filters={"name": data.name})

            if exists:
                errors.append(
                    {
                        "loc": ("body", "name"),
                        "msg": ProductEntity.NAME_IN_USE.value,
                        "type": "domain_validation",
                    }
                )

        # Validar que cada elemento de la lista de imágenes sea una URL válida
        if data.images:
            adapter = TypeAdapter(HttpUrl)

            for i, url in enumerate(data.images):
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
        if data.categories:
            for i, category in enumerate(data.categories):
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
