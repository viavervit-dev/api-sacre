from fastapi.exceptions import RequestValidationError
from pydantic import HttpUrl, TypeAdapter

from src.api.common.utils import FinancialCalculationsMixin
from src.api.modules.inventory.constants import ProductEntity
from src.api.modules.inventory.dto import CreateProductPublicDTO, ReadProductPrivateDTO
from src.api.modules.inventory.repositories.interfaces import (
    ICategoryRepository,
    IProductRepository,
)


class CreateProductPublicService(FinancialCalculationsMixin):
    """Servicio encargado de la creación de productos para el catálogo público."""

    def __init__(
        self,
        product_repo: IProductRepository,
        category_repo: ICategoryRepository,
    ) -> None:
        self.__product_repo = product_repo
        self.__category_repo = category_repo

    async def create(self, data: CreateProductPublicDTO) -> ReadProductPrivateDTO:
        """
        Crea un nuevo producto para el catálogo público.

        Raises:
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        # Ejecutamos validaciones de las reglas de negocio
        await self.__run_business_validations(data=data)

        # Asignar el estado del producto según el stock total
        product_data = data.model_dump()

        if product_data["stock_total"] > 0:
            product_data["status"] = True
        else:
            product_data["status"] = False

        # Calcular el precio de venta
        product_data["price_sale"] = self._calculate_sale_price_product(
            price_neto=product_data["price_neto"],
            profit_margin=product_data["profit_margin"],
        )

        # Calcular el monto del IVA
        product_data["tax_amount"] = self._calculate_tax_amount(amount=product_data["price_sale"])

        # Inicializar el stock en mano, el stock de venta y exclusividad
        product_data["stock_sale"] = product_data["stock_total"]
        product_data["exclusive"] = False
        product_data["stock_hand"] = 0

        product = await self.__product_repo.create_product(data=product_data)

        return ReadProductPrivateDTO.model_construct(**product.to_dict())

    async def __run_business_validations(self, data: CreateProductPublicDTO) -> None:
        """
        Ejecuta las validaciones de negocio previas a la creación del producto.

        Raises:
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
