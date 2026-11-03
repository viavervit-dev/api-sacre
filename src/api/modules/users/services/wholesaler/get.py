from uuid import UUID

from src.api.common.exceptions import ResourceNotFound
from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.repositories.interfaces import IUserRepository
from src.api.modules.users.dto import ReadWholesalerDTO


class GetWholesalerService:
    """Servicio encargado de la consulta y obtención del detalle de un cliente mayorista."""

    def __init__(self, user_repo: IUserRepository) -> None:
        self.__user_repo = user_repo

    async def get(self, wholesaler_id: UUID) -> ReadWholesalerDTO:
        """
        Obtiene el detalle completo de un cliente mayorista por su identificador único.

        Raises:
            ResourceNotFound: Si el cliente mayorista no existe en la base de datos.
        """

        # Validar que el cliente mayorista exista en la base de datos
        user = await self.__user_repo.get_user(
            load_permissions=False,
            filters={
                "role": UserRoles.WHOLESALER.value,
                "id": wholesaler_id,
            },
        )

        if not user:
            raise ResourceNotFound()

        # Instanciar el DTO de respuesta
        wholesaler_data = user.wholesaler.to_dict()
        wholesaler_data["id"] = user.id
        wholesaler_data["email"] = user.email

        return ReadWholesalerDTO.model_construct(**wholesaler_data)
