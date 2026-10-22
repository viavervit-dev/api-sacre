from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.repositories.interfaces import IUserRepository
from src.api.modules.users.dto import ReadCustomerWholesaleDTO


class GetListCustomerWholesaleService:
    """Servicio encargado de la consulta y serialización de clientes mayoristas."""

    def __init__(self, user_repo: IUserRepository) -> None:
        self.__user_repo = user_repo

    async def get_list(
        self,
        offset: int,
        limit: int,
    ) -> tuple[list[ReadCustomerWholesaleDTO], int]:
        """Obtiene una lista paginada de clientes mayoristas y el total de registros."""

        users, total_items = await self.__user_repo.get_list_users(
            filters={"role": UserRoles.CUSTOMER_WHOLESALE.value},
            load_permissions=False,
            offset=offset,
            limit=limit,
        )

        if not users:
            return [], 0

        result = []

        for user in users:
            user_data = user.to_dict()
            user_data.pop("date_joined")
            profile_data = user.customer_wholesale.to_dict()
            profile_data.pop("id")
            profile_data.pop("date_joined")
            dto = ReadCustomerWholesaleDTO.model_construct(**user_data, **profile_data)
            result.append(dto)

        return result, total_items
