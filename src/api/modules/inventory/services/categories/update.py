from typing import Any
from uuid import UUID

from fastapi.exceptions import RequestValidationError

from src.api.common.exceptions import ResourceNotFound
from src.api.modules.inventory.constants import CategoryEntity
from src.api.modules.inventory.dto import ReadCategoryPrivateDTO, UpdateCategoryDTO
from src.api.modules.inventory.repositories.interfaces import ICategoryRepository


class UpdateCategoryService:
    """Servicio encargado de la actualización de categorías de productos."""

    def __init__(self, category_repo: ICategoryRepository) -> None:
        self.__category_repo = category_repo

    async def update(
        self,
        data: UpdateCategoryDTO,
        category_id: UUID,
    ) -> ReadCategoryPrivateDTO:
        """
        Actualiza una categoría tras validar las reglas de negocio del dominio.

        Raises:
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
            ResourceNotFound: Si la categoría no existe en la base de datos.
        """

        category_data = data.model_dump(exclude_unset=True)
        instance = await self.__category_repo.get_category_by_id(id=category_id)

        if not instance:
            raise ResourceNotFound()

        await self.__run_business_validations(data=category_data)

        # Actualizar el producto en la base de datos
        category = await self.__category_repo.update_category(
            data=category_data,
            instance=instance,
        )

        return ReadCategoryPrivateDTO.model_construct(**category.to_dict())

    async def __run_business_validations(self, data: dict[str, Any]) -> None:
        """
        Ejecuta las validaciones de reglas de negocio previas a la actualización.

        Raises:
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
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
