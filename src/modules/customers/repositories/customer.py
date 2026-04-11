from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.authentication.models.permission import Group
from src.modules.authentication.models.user import User, UserGroup
from src.modules.customers.constants import ROLE
from src.modules.customers.dto import CustomerCreateDTO, CustomerReadDTO
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
        data: CustomerCreateDTO,
        session: AsyncSession,
    ) -> CustomerReadDTO:

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

        await session.flush()  # Para obtener el customer.id

        await session.commit()
        await session.refresh(customer)

        return CustomerReadDTO(
            id=customer.user_id,
            first_names=customer.first_names,
            last_names=customer.last_names,
            document_type=customer.document_type,
            document_number=customer.document_number,
            phone=customer.phone,
        )
