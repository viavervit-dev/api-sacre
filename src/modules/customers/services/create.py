from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.constants import UserRoles
from src.modules.auth.dto import ReadUserDTO
from src.modules.auth.repositories.interfaces import IUserRepository
from src.modules.customers.dto import CreateCustomerDTO, ReadCustomerDTO


class CreateCustomerService:
    """Servicio para la creación de clientes en la base de datos."""

    def __init__(self, user_repo: type[IUserRepository], db: AsyncSession) -> None:
        self.__user_repo = user_repo
        self.__db = db

    async def create_customer(self, data: CreateCustomerDTO) -> ReadUserDTO[ReadCustomerDTO]:
        """Crea un nuevo cliente en la base de datos."""

        # Extrae los campos de usuario y perfil del DTO de entrada para pasarlos al repositorio
        user_fields = ["email", "password"]
        profile_fields = ["first_names", "last_names", "document_type", "document_number", "phone"]
        user_data = {field: getattr(data, field) for field in user_fields}
        profile_data = {field: getattr(data, field) for field in profile_fields}
        user_data["session_version"] = 1

        user_instance, profile_instance = await self.__user_repo.create_user(
            db=self.__db,
            user_data=user_data,
            profile_data=profile_data,
            role=UserRoles.CUSTOMER.value,
        )
        profile = ReadCustomerDTO.model_construct(
            first_names=profile_instance.first_names,
            last_names=profile_instance.last_names,
            document_type=profile_instance.document_type,
            document_number=profile_instance.document_number,
            phone=profile_instance.phone,
        )
        user = ReadUserDTO[ReadCustomerDTO].model_construct(
            id=user_instance.id,
            email=user_instance.email,
            role_data=profile,
        )

        return user
