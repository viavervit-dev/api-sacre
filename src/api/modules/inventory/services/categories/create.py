from fastapi.exceptions import RequestValidationError

from src.api.modules.inventory.constants import CategoryEntity
from src.api.modules.inventory.dto import CreateCategoryDTO, ReadCategoryPrivateDTO
from src.api.modules.inventory.repositories.interfaces import ICategoryRepository


class CreateCategoryService:
    """Servicio encargado de la creación de categorías de productos."""

    def __init__(self, category_repo: ICategoryRepository) -> None:
        self.__category_repo = category_repo

    async def create(self, data: CreateCategoryDTO) -> ReadCategoryPrivateDTO:
        """
        Crea una nueva categoría aplicando valores iniciales y validaciones de negocio.

        Raises:
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        # Ejecutamos validaciones de las reglas de negocio
        await self.__run_business_validations(data=data)

        category_data = data.model_dump()

        # Asignar el estado del producto según el stock total
        category_data["status"] = False

        category = await self.__category_repo.create_category(data=category_data)

        return ReadCategoryPrivateDTO.model_construct(**category.to_dict())

    async def __run_business_validations(self, data: CreateCategoryDTO) -> None:
        """
        Ejecuta las validaciones de reglas de negocio previas a la creación.

        Raises:
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        # Validar que el nombre de la categoría no esté registrado en la base de datos
        if data.name:
            exists = await self.__category_repo.exists_category(filters={"name": data.name})

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
