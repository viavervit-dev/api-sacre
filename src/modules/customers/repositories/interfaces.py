from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.customers.dto import CreateCustomerDTO, ReadCustomerDTO


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
        data: CreateCustomerDTO,
        session: AsyncSession,
    ) -> ReadCustomerDTO:
        """Crea un nuevo cliente en la base de datos a partir de un diccionario de datos y se le
        asigna el rol **customer**."""

        pass

    @classmethod
    @abstractmethod
    async def exists(cls, session: AsyncSession, **kwargs: Any) -> bool:
        """Consulta si existe al menos un registro que coincida con los filtros proporcionados."""

        pass

    @classmethod
    @abstractmethod
    async def get_customer(cls, session: AsyncSession, **kwargs: Any) -> list[ReadCustomerDTO]:
        """Obtiene una lista de clientes que coincidan con los filtros proporcionados."""

        pass
