from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.customers.dto import ReadCustomerDTO


class IAdminRepository(ABC):
    """
    Interfaz de `AdminRepository`, define el contrato para un repositorio que administra la tabla
    `admin.admins` en la base de datos. Esta clase proporciona métodos que realizan operaciones
    CRUD entre otros tipos de consultas.
    """

    @classmethod
    @abstractmethod
    async def get_admin(cls, session: AsyncSession, **kwargs: Any) -> list[ReadCustomerDTO]:
        """Obtiene una lista de administradores que coincidan con los filtros proporcionados."""

        pass
