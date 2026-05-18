from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.authentication.models.user import User
from src.modules.customers.dto import ReadCustomerDTO
from src.modules.customers.models.customer import Customer
from src.modules.customers.repositories.interfaces import ICustomerRepository


class CustomerRepository(ICustomerRepository):
    """
    Interfaz de `CustomerRepository`, define el contrato para un repositorio que administra la
    tabla `customer.customers` en la base de datos. Esta clase proporciona métodos que realizan
    operaciones CRUD entre otros tipos de consultas.
    """

    @classmethod
    async def get_customer(cls, session: AsyncSession, **kwargs: Any) -> list[ReadCustomerDTO]:

        user_filters = []
        customer_filters = []

        # Clasificar los filtros según si pertenecen al modelo Customer o User
        for key, value in kwargs.items():
            if hasattr(Customer, key):
                customer_filters.append(getattr(Customer, key) == value)
            elif hasattr(User, key):
                user_filters.append(getattr(User, key) == value)
            else:
                raise ValueError(f"No existe la columna '{key}' en los modelos Customer y User.")

        # Construir la consulta dinámica según los filtros proporcionados
        stmt = select(Customer)

        if user_filters:
            stmt = stmt.join(User).where(*user_filters)
        if customer_filters:
            stmt = stmt.where(*customer_filters)

        result = await session.execute(stmt)

        customers = result.scalars().all()

        return [
            ReadCustomerDTO.model_construct(
                id=customer.user_id,
                first_names=customer.first_names,
                last_names=customer.last_names,
                document_type=customer.document_type,
                document_number=customer.document_number,
                phone=customer.phone,
            )
            for customer in customers
        ]
