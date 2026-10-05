from typing import Any

from fastapi.exceptions import RequestValidationError

from src.modules.inventory.constants import CategoryEntity
from src.modules.inventory.dto import CreateCategoryDTO, PrivateReadCategoryDTO
from src.modules.inventory.repositories.interfaces import ICategoryRepository


class CreateCategoryService:
    """Servicio encargado de la validación de negocio y persistencia para nuevas categorías."""

    def __init__(self, category_repo: ICategoryRepository) -> None:
        self.__category_repo = category_repo

    async def create_category(self, data: CreateCategoryDTO) -> PrivateReadCategoryDTO:
        """
        Crea una nueva categoría aplicando valores iniciales y validaciones de negocio.

        Raises:
            RequestValidationError: Si falla alguna validacion de negocio.
        """

        category_data = data.model_dump()
        category_data["status"] = False  # Asignar estado activo por defecto
        category_data["product_count"] = 0  # Asignar contador de productos por defecto
        await self.__run_business_validations(data=category_data)
        category_instance = await self.__category_repo.create_category(data=category_data)
        category = PrivateReadCategoryDTO.model_construct(
            id=category_instance.id,
            name=category_instance.name,
            description=category_instance.description,
            product_count=category_instance.product_count,
            status=category_instance.status,
        )

        return category

    async def __run_business_validations(self, data: dict[str, Any]) -> None:
        """
        Ejecuta las validaciones de reglas de negocio previas a la creación.

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
