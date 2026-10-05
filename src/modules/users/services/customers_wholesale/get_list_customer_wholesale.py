from src.modules.users.dto import ReadCustomerWholesaleDTO
from src.modules.users.repositories.interfaces import ICustomerWholesaleRepository


class RetrieveListCustomerWholesaleService:
    """Servicio encargado de la consulta y serialización de clientes mayoristas."""

    def __init__(self, customer_wholesale_repo: ICustomerWholesaleRepository) -> None:
        self.__customer_wholesale_repo = customer_wholesale_repo

    async def get_customers_wholesale(
        self,
        offset: int,
        limit: int,
    ) -> tuple[list[ReadCustomerWholesaleDTO], int]:
        """Obtiene una lista paginada de clientes mayoristas y el total de registros."""

        (
            customers_wholesale,
            total_items,
        ) = await self.__customer_wholesale_repo.get_customers_wholesale(
            offset=offset,
            limit=limit,
        )

        if not customers_wholesale:
            return [], 0

        result = []

        for customer_wholesale in customers_wholesale:
            dto = ReadCustomerWholesaleDTO.model_construct(
                id=customer_wholesale.id,
                email=customer_wholesale.email,
                name_or_company_name=customer_wholesale.name_or_company_name,
                ruc=customer_wholesale.ruc,
                phone=customer_wholesale.phone,
                location=customer_wholesale.location,
                extra_contacts=customer_wholesale.extra_contacts,
            )
            result.append(dto)

        return result, total_items
