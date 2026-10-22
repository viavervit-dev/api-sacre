from uuid import UUID

from src.api.common.exceptions import ResourceNotFound
from src.api.modules.inventory.repositories.interfaces import ICategoryRepository


class DeleteCategoryService:
    """Servicio encargado de la eliminación de categorías de productos."""

    def __init__(self, category_repo: ICategoryRepository) -> None:
        self.__category_repo = category_repo

    async def delete(self, category_id: UUID) -> None:
        """
        Elimina una categoría tras validar las reglas de negocio del dominio.

        Raises:
            DomainRuleViolation: Si falla alguna validación de las reglas de negocio.
            ResourceNotFound: Si la categoría no existe en la base de datos.
        """

        # Validar que la categoría exista en la base de datos
        category = await self.__category_repo.get_category_by_id(id=category_id)

        if not category:
            raise ResourceNotFound()

        await self.__category_repo.delete_category(instance=category)
