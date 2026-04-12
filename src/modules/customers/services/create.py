from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.customers.dto import CreateCustomerDTO, ReadCustomerDTO
from src.modules.customers.repositories.interfaces import ICustomerRepository


class CreateCustomerService:
    """Servicio para la creación de clientes en la base de datos."""

    def __init__(self, customer_repo: ICustomerRepository, session: AsyncSession) -> None:
        self.customer_repo = customer_repo
        self.session = session

    async def create_customer(self, data: CreateCustomerDTO) -> ReadCustomerDTO:
        """Crea un nuevo cliente en la base de datos."""

        customer = await self.customer_repo.create_customer(data=data, session=self.session)

        return customer
