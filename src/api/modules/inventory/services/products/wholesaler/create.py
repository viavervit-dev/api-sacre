from uuid import UUID

from fastapi.exceptions import RequestValidationError

from src.api.common.exceptions import ResourceNotFound
from src.api.common.utils import FinancialCalculationsMixin
from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.repositories.interfaces import IUserRepository
from src.api.modules.inventory.constants import ProductEntity
from src.api.modules.inventory.dto import CreateWholesalerProductDTO, ReadWholesalerProductDTO
from src.api.modules.inventory.models.wholesaler_product import WholesalerProduct
from src.api.modules.inventory.repositories.interfaces import (
    ICategoryRepository,
    IWholesalerProductRepository,
)


class AddProductWholesalerService(FinancialCalculationsMixin):
    """Servicio encargado de la creación de productos exclusivos para mayoristas."""

    def __init__(
        self,
        user_repo: IUserRepository,
        wholesaler_product_repo: IWholesalerProductRepository,
        category_repo: ICategoryRepository,
    ) -> None:
        self.__user_repo = user_repo
        self.__wholesaler_product_repo = wholesaler_product_repo
        self.__category_repo = category_repo

    async def add_product(
        self,
        data: CreateWholesalerProductDTO,
        wholesaler_id: UUID,
    ) -> ReadWholesalerProductDTO:
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
        product = await self.__create_product(data=data, wholesaler_id=wholesaler_id)

        return ReadWholesalerProductDTO.model_construct(**product.to_dict())

    async def __create_product(
        self,
        data: CreateWholesalerProductDTO,
        wholesaler_id: UUID,
    ) -> WholesalerProduct:
        """
        Crea un nuevo producto para un cliente mayorista.

        Raises:
            RequestValidationError: Si falla alguna validacion de negocio.
        """

        # Ejecutamos validaciones de las reglas de negocio
        await self.__run_business_validations(data=data)

        # Inicializar algunos valores por defecto
        product_data = data.model_dump()
        product_data["status"] = True

        return await self.__wholesaler_product_repo.create_product(
            wholesaler_id=wholesaler_id,
            data=product_data,
        )

    async def __run_business_validations(self, data: CreateWholesalerProductDTO) -> None:
        """
        Ejecuta las validaciones de negocio previas al registro del producto.

        Raises:s
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        errors = []

        # Validar que el nombre del producto no esté registrado en la base de datos
        if data.name:
            exists = await self.__wholesaler_product_repo.exists_product(
                filters={"name": data.name},
            )

            if exists:
                errors.append(
                    {
                        "loc": ("body", "name"),
                        "msg": ProductEntity.NAME_IN_USE.value,
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
