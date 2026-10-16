from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.repositories.interfaces import IUserRepository
from src.api.modules.users.dto import ReadCustomerWholesaleDTO


class GetListCustomerWholesaleService:
    """Servicio encargado de la consulta y serialización de clientes mayoristas."""

    def __init__(self, user_repo: IUserRepository) -> None:
        self.__user_repo = user_repo

    async def get_customers_wholesale(
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
            dto = ReadCustomerWholesaleDTO.model_construct(
                id=user.id,
                email=user.email,
                name_or_company_name=user.customer_wholesale.name_or_company_name,
                ruc=user.customer_wholesale.ruc,
                phone=user.customer_wholesale.phone,
                location=user.customer_wholesale.location,
                extra_contacts=user.customer_wholesale.extra_contacts,
            )
            result.append(dto)

        return result, total_items
