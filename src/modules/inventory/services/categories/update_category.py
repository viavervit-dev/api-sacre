from typing import Any
from uuid import UUID

from fastapi.exceptions import RequestValidationError

from src.common.exceptions import ResourceNotFound
from src.modules.inventory.constants import CategoryEntity
from src.modules.inventory.dto import PrivateReadCategoryDTO, UpdateCategoryDTO
from src.modules.inventory.repositories.interfaces import ICategoryRepository


class UpdateCategoryService:
    """Servicio encargado de la validación de negocio y actualización de categorías."""

    def __init__(self, category_repo: ICategoryRepository) -> None:
        self.__category_repo = category_repo

    async def update_category(
        self,
        data: UpdateCategoryDTO,
        category_id: UUID,
    ) -> PrivateReadCategoryDTO:
        """
        Actualiza una categoría tras validar las reglas de negocio del dominio.

        Raises:
            RequestValidationError: Si falla alguna validacion de negocio.
            ResourceNotFound: Si la categoría no existe en la base de datos.
        """

        category_data = data.model_dump(exclude_unset=True)
        instance = await self.__category_repo.get_category(id=category_id)

        if not instance:
            raise ResourceNotFound()

        await self.__run_business_validations(data=category_data)

        # Actualizar el producto en la base de datos
        instance = await self.__category_repo.update_category(
            data=category_data,
            instance=instance,
        )
        category = PrivateReadCategoryDTO.model_construct(
            id=instance.id,
            name=instance.name,
            description=instance.description,
            product_count=instance.product_count,
            status=instance.status,
        )

        return category

    async def __run_business_validations(self, data: dict[str, Any]) -> None:
        """
        Ejecuta las validaciones de reglas de negocio previas a la actualización.

        Raises:
            RequestValidationError: Si falla alguna validacion de negocio.
        """

        # Validar que el nombre de la categoría no esté registrado en la base de datos
        if data.get("name"):
            exists = await self.__category_repo.exists_category(filters={"name": data["name"]})

            if exists:
                raise RequestValidationError(
                    errors=[
                        {
                            "loc": ("body", "name"),
                            "msg": CategoryEntity.NAME_IN_USE.value,
                            "type": "domain_validation",
                        }
                    ]
                )
