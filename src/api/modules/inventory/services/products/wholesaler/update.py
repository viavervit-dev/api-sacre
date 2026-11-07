from uuid import UUID

from fastapi.exceptions import RequestValidationError

from src.api.common.exceptions import ResourceNotFound
from src.api.modules.inventory.constants import ProductEntity
from src.api.modules.inventory.dto import ReadWholesalerProductDTO, UpdateWholesalerProductDTO
from src.api.modules.inventory.repositories.interfaces import (
    ICategoryRepository,
    IWholesalerProductRepository,
)


class UpdateProductWholesalerService:
    """Servicio encargado de la actualización de productos para clientes mayoristas."""

    def __init__(
        self,
        wholesaler_product_repo: IWholesalerProductRepository,
        category_repo: ICategoryRepository,
    ) -> None:
        self.__wholesaler_product_repo = wholesaler_product_repo
        self.__category_repo = category_repo

    async def update(
        self,
        data: UpdateWholesalerProductDTO,
        product_id: UUID,
    ) -> ReadWholesalerProductDTO:
        """
        Actualiza un producto para un cliente mayorista.

        Raises:
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
            ResourceNotFound: Si el producto no existe en la base de datos.
        """

        # Validar que el producto exista en la base de datos
        product = await self.__wholesaler_product_repo.get_product_by_id(id=product_id)

        if not product:
            raise ResourceNotFound()

        # Ejecutamos validaciones de las reglas de negocio
        await self.__run_business_validations(data=data)

        # Actualizar el producto en la base de datos
        updated_product = await self.__wholesaler_product_repo.update_product(
            data=data.model_dump(exclude_unset=True),
            instance=product,
        )

        return ReadWholesalerProductDTO.model_construct(**updated_product.to_dict())

    async def __run_business_validations(self, data: UpdateWholesalerProductDTO) -> None:
        """
        Ejecuta las validaciones de negocio previas a la actualización del producto.

        Raises:
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
