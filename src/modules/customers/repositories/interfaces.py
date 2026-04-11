from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.customers.dto import CustomerCreateDTO, CustomerReadDTO


class ICustomerRepository(ABC):
    """
    Interfaz de `CustomerRepository`, define el contrato para un repositorio que administra la
    tabla `customer.customers` en la base de datos. Esta clase proporciona métodos que realizan
    operaciones CRUD entre otros tipos de consultas.
    """

    @classmethod
    @abstractmethod
    async def create_customer(
        cls,
        data: CustomerCreateDTO,
        session: AsyncSession,
    ) -> CustomerReadDTO:
        """Crea un nuevo cliente en la base de datos a partir de un diccionario de datos."""

        pass
