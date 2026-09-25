from uuid import UUID

from src.common.exceptions import DomainRuleViolation, ResourceNotFound
from src.modules.inventory.constants import ExceptionErrorMessages
from src.modules.inventory.models.category import Category
from src.modules.inventory.repositories.interfaces import ICategoryRepository


class DeleteCategoryService:
    """Servicio encargado de la validación de negocio y eliminación de categorías."""

    def __init__(self, category_repo: ICategoryRepository) -> None:
        self.__category_repo = category_repo

    async def delete_category(self, category_id: UUID) -> None:
        """
        Elimina una categoría tras validar las reglas de negocio del dominio.

        Raises:
            DomainRuleViolation: Si la categoría tiene productos asociados.
            ResourceNotFound: Si la categoría no existe en la base de datos.
        """

        instance = await self.__category_repo.get_category(id=category_id)

        if not instance:
            raise ResourceNotFound()

        await self.__run_business_validations(instance=instance)
        await self.__category_repo.delete_category(instance=instance)

    async def __run_business_validations(self, instance: Category) -> None:
        """
        Valida que la categoría cumpla las condiciones requeridas para su eliminación.

        Raises:
            DomainRuleViolation: Si la categoría cuenta con productos asociados.
        """

        # Validar que la categoría no tenga productos asociados antes de eliminarla
        if instance.product_count > 0:
            raise DomainRuleViolation(
                message=ExceptionErrorMessages.CATEGORY_HAS_DEPENDENCIES.value
            )
