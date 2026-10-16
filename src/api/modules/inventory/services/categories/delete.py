from uuid import UUID

from src.api.common.exceptions import ResourceNotFound
from src.api.modules.inventory.repositories.interfaces import ICategoryRepository


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

        instance = await self.__category_repo.get_category_by_id(id=category_id)

        if not instance:
            raise ResourceNotFound()

        await self.__category_repo.delete_category(instance=instance)
