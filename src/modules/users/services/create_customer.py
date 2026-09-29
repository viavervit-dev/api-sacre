from typing import Any

from fastapi.exceptions import RequestValidationError

from src.modules.auth.constants import UserEntity, UserRoles
from src.modules.auth.dto import ReadUserDTO
from src.modules.auth.repositories.interfaces import IUserRepository
from src.modules.users.constants import CustomerEntity
from src.modules.users.dto import CreateCustomerDTO
from src.modules.users.repositories.interfaces import ICustomerRepository


class CreateCustomerService:
    """Servicio encargado de la validación de negocio y registro de clientes."""

    def __init__(self, user_repo: IUserRepository, customer_repo: ICustomerRepository) -> None:
        self.__customer_repo = customer_repo
        self.__user_repo = user_repo

    async def create_customer(self, data: CreateCustomerDTO) -> ReadUserDTO:
        """
        Registra un nuevo cliente tras validar las reglas de negocio del dominio.

        Raises:
            RequestValidationError: Si falla alguna validacion de negocio.
        """

        # Validaciones de negocio
        await self.__run_business_validations(data=data.model_dump())

        # Creamos el usuario base con su rol y permisos
        user_instance = await self.__user_repo.create_user(
            email=data.email,
            password=data.password,
            role=UserRoles.CUSTOMER.value,
        )

        # Creamos el perfil de cliente con el ID del usuario
        profile_data = {
            "first_names": data.first_names,
            "last_names": data.last_names,
            "document_type": data.document_type,
            "document_number": data.document_number,
            "phone": data.phone,
        }
        profile_instance = await self.__customer_repo.create_customer(
            user_id=user_instance.id,
            data=profile_data,
        )
        user_instance.customer = profile_instance

        return ReadUserDTO.model_construct(
            id=user_instance.id,
            first_names=profile_instance.first_names,
            last_names=profile_instance.last_names,
            email=user_instance.email,
            role=user_instance.role,
        )

    async def __run_business_validations(self, data: dict[str, Any]) -> None:
        """
        Ejecuta las validaciones de negocio previas al registro del cliente.

        Raises:
            RequestValidationError: Si falla alguna validacion de negocio.
        """

        errors = []

        # Validar que el correo electrónico no esté registrado en la base de datos
        exists = await self.__user_repo.exists_user(filters={"email": data["email"]})

        if exists:
            errors.append(
                {
                    "loc": ("body", "email"),
                    "msg": UserEntity.EMAIL_IN_USE.value,
                    "type": "domain_validation",
                }
            )

        # Validar que el número de teléfono no esté registrado en la base de datos
        exists = await self.__customer_repo.exists_customer(filters={"phone": data["phone"]})

        if exists:
            errors.append(
                {
                    "loc": ("body", "phone"),
                    "msg": CustomerEntity.PHONE_IN_USE.value,
                    "type": "domain_validation",
                }
            )

        # Validar que el número de documento no esté registrado en la base de datos
        exists = await self.__customer_repo.exists_customer(
            filters={"document_number": data["document_number"]},
        )

        if exists:
            errors.append(
                {
                    "loc": ("body", "document_number"),
                    "msg": CustomerEntity.DOCUMENT_NUMBER_IN_USE.value,
                    "type": "domain_validation",
                }
            )

        if errors:
            raise RequestValidationError(errors=errors)
