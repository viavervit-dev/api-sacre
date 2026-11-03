from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.repositories.interfaces import IUserRepository
from src.api.modules.users.dto import ReadWholesalerSummaryDTO


class GetListWholesalerService:
    """Servicio encargado de consultar la lista de clientes mayoristas."""

    def __init__(self, user_repo: IUserRepository) -> None:
        self.__user_repo = user_repo

    async def get_list(
        self,
        offset: int,
        limit: int,
    ) -> tuple[list[ReadWholesalerSummaryDTO], int]:
        """Obtiene una lista paginada de clientes mayoristas y el total de registros."""

        users, total_items = await self.__user_repo.get_list_users(
            filters={"role": UserRoles.WHOLESALER.value},
            load_permissions=False,
            offset=offset,
            limit=limit,
        )

        if not users:
            return [], 0

        result = []

        for user in users:
            profile_data = user.wholesaler.to_dict()
            profile_data["id"] = user.id
            dto = ReadWholesalerSummaryDTO.model_construct(**profile_data)
            result.append(dto)

        return result, total_items
