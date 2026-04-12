from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.authentication.models.permission import Group
from src.modules.authentication.models.user import User, UserGroup
from src.modules.customers.constants import ROLE
from src.modules.customers.dto import CreateCustomerDTO, ReadCustomerDTO
from src.modules.customers.models.customer import Customer
from src.modules.customers.repositories.interfaces import ICustomerRepository


class CustomerRepository(ICustomerRepository):
    """
    Interfaz de `CustomerRepository`, define el contrato para un repositorio que administra la
    tabla `customer.customers` en la base de datos. Esta clase proporciona métodos que realizan
    operaciones CRUD entre otros tipos de consultas.
    """

    @classmethod
    async def create_customer(
        cls,
        data: CreateCustomerDTO,
        session: AsyncSession,
    ) -> ReadCustomerDTO:

        user = User(email=data.email)  # pyright: ignore[reportCallIssue]
        user.set_password(data.password)
        session.add(user)

        await session.flush()

        # Asignar el rol "customer" al nuevo usuario
        result = await session.execute(select(Group).filter_by(name=ROLE))
        customer_group = result.scalar_one_or_none()

        if not customer_group:
            raise ValueError(f"El rol '{ROLE}' no existe en la base de datos.")

        user_group = UserGroup(user_id=user.id, group_id=customer_group.id)
        session.add(user_group)
        await session.flush()

        customer = Customer(
            user_id=user.id,
            first_names=data.first_names,
            last_names=data.last_names,
            document_type=data.document_type,
            document_number=data.document_number,
            phone=data.phone,
        )
        session.add(customer)

        await session.flush()

        await session.commit()
        await session.refresh(customer)

        return ReadCustomerDTO(
            id=customer.user_id,
            first_names=customer.first_names,
            last_names=customer.last_names,
            document_type=customer.document_type,
            document_number=customer.document_number,
            phone=customer.phone,
        )

    @classmethod
    async def exists(cls, session: AsyncSession, **kwargs: Any) -> bool:

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
        if user_filters and not customer_filters:
            stmt = select(select(User.id).where(*user_filters).exists())
        else:
            stmt = select(Customer.user_id)
            if user_filters:
                stmt = stmt.join(User).where(*user_filters)
            if customer_filters:
                stmt = stmt.where(*customer_filters)

            stmt = select(stmt.exists())

        result = await session.execute(stmt)

        return result.scalar_one()
