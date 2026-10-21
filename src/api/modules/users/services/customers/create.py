from fastapi.exceptions import RequestValidationError

from src.api.modules.auth.constants import UserEntity, UserRoles
from src.api.modules.auth.dto import ReadUserDTO
from src.api.modules.auth.repositories.interfaces import IUserRepository
from src.api.modules.users.constants import CustomerEntity
from src.api.modules.users.dto import CreateCustomerDTO
from src.api.modules.users.repositories.interfaces import ICustomerRepository


class CreateCustomerService:
    """Servicio encargado de la validación de negocio y registro de clientes."""

    def __init__(self, user_repo: IUserRepository, customer_repo: ICustomerRepository) -> None:
        self.__customer_repo = customer_repo
        self.__user_repo = user_repo

    async def create(self, data: CreateCustomerDTO) -> ReadUserDTO:
        """
        Registra un nuevo cliente tras validar las reglas de negocio del dominio.

        Raises:
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        # Validaciones de negocio
        await self.__run_business_validations(data=data)

        # Creamos el usuario base con su rol y permisos
        customer_data = data.model_dump()
        user_instance = await self.__user_repo.create_user(
            email=customer_data.pop("email"),
            password=customer_data.pop("password"),
            role=UserRoles.CUSTOMER.value,
        )
        profile_instance = await self.__customer_repo.create_customer(
            user_id=user_instance.id,
            data=customer_data,
        )
        user_instance.customer = profile_instance

        # Instanciar el DTO de respuesta
        customer_data = profile_instance.to_dict()
        customer_data["id"] = user_instance.id
        customer_data["role"] = user_instance.role

        return ReadUserDTO.model_construct(**customer_data)

    async def __run_business_validations(self, data: CreateCustomerDTO) -> None:
        """
        Ejecuta las validaciones de negocio previas al registro del cliente.

        Raises:
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        errors = []

        # Validar que el correo electrónico no esté registrado en la base de datos
        if data.email:
            exists = await self.__user_repo.exists_user(filters={"email": data.email})

            if exists:
                errors.append(
                    {
                        "loc": ("body", "email"),
                        "msg": UserEntity.EMAIL_IN_USE.value,
                        "type": "domain_validation",
                    }
                )

        # Validar que el número de teléfono no esté registrado en la base de datos
        if data.phone:
            exists = await self.__customer_repo.exists_customer(filters={"phone": data.phone})

            if exists:
                errors.append(
                    {
                        "loc": ("body", "phone"),
                        "msg": CustomerEntity.PHONE_IN_USE.value,
                        "type": "domain_validation",
                    }
                )

        # Validar que el número de documento no esté registrado en la base de datos
        if data.document_number:
            exists = await self.__customer_repo.exists_customer(
                filters={"document_number": data.document_number},
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
