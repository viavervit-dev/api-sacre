from uuid import UUID

from src.api.common.exceptions import DomainRuleViolation, ResourceNotFound
from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.models import User
from src.api.modules.inventory.constants import ExceptionErrorMessages
from src.api.modules.inventory.dto import ReadProductPrivateDTO, ReadProductPublicDTO
from src.api.modules.inventory.repositories.interfaces import IProductRepository


class GetProductService:
    """Servicio encargado de la consulta del detalle de un producto."""

    def __init__(self, product_repo: IProductRepository) -> None:
        self.__product_repo = product_repo

    async def get(
        self,
        user: User | None,
        product_id: UUID,
    ) -> ReadProductPrivateDTO | ReadProductPublicDTO:
        """
        Obtiene el detalle de un producto según el nivel de visibilidad del usuario solicitante.

        Raises:
            ResourceNotFound: Si el producto no existe en la base de datos.
            DomainRuleViolation: Si el producto no cumple las reglas de visibilidad requeridas.
        """

        # Validar que el producto exista en la base de datos
        product = await self.__product_repo.get_product_by_id(id=product_id)

        if not product:
            raise ResourceNotFound()

        # Validar que el producto sea visible para el usuario según su rol
        if not user or user.role != UserRoles.ADMINISTRATOR.value:
            product_status = product.status

            if not product_status:
                raise DomainRuleViolation(
                    message=ExceptionErrorMessages.PRODUCT_NOT_AVAILABLE.value
                )

            return ReadProductPublicDTO.model_construct(**product.to_dict())

        return ReadProductPrivateDTO.model_construct(**product.to_dict())
