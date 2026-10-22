import secrets

from fastapi.exceptions import RequestValidationError

from src.api.modules.auth.constants import UserEntity, UserRoles
from src.api.modules.auth.repositories.interfaces import IUserRepository
from src.api.modules.users.constants import CustomerWholesaleEntity
from src.api.modules.users.dto import CreateCustomerWholesaleDTO, ReadCustomerWholesaleDTO
from src.api.modules.users.repositories.interfaces import ICustomerWholesaleRepository


class CreateCustomerWholesaleService:
    """Servicio encargado de la validación de negocio y registro de clientes mayoristas."""

    def __init__(
        self,
        customer_wholesale_repo: ICustomerWholesaleRepository,
        user_repo: IUserRepository,
    ) -> None:
        self.__customer_wholesale_repo = customer_wholesale_repo
        self.__user_repo = user_repo

    async def create(self, data: CreateCustomerWholesaleDTO) -> ReadCustomerWholesaleDTO:
        """
        Registra un nuevo cliente mayorista tras validar las reglas de negocio del dominio.

        Raises:
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        # Ejecutar validaciones de las reglas de negocio
        await self.__run_business_validations(data=data)

        # Creamos el usuario base con su rol y permisos
        customer_wholesale_data = data.model_dump()
        customer_wholesale_data["products"] = []
        user_instance = await self.__user_repo.create_user(
            email=customer_wholesale_data.pop("email"),
            password=secrets.token_urlsafe(nbytes=12),
            role=UserRoles.CUSTOMER_WHOLESALE.value,
        )
        profile_instance = await self.__customer_wholesale_repo.create_customer_wholesale(
            user_id=user_instance.id,
            data=customer_wholesale_data,
        )
        user_instance.customer_wholesale = profile_instance

        # Instanciar el DTO de respuesta
        customer_wholesale_data = profile_instance.to_dict()
        customer_wholesale_data["id"] = user_instance.id
        customer_wholesale_data["email"] = user_instance.email

        return ReadCustomerWholesaleDTO.model_construct(**customer_wholesale_data)

    async def __run_business_validations(self, data: CreateCustomerWholesaleDTO) -> None:
        """
        Ejecuta las validaciones de negocio previas al registro del cliente mayorista.

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

        # Validar que el nombre o razón social no esté registrado en la base de datos
        if data.name_or_company_name:
            exists = await self.__customer_wholesale_repo.exists_customer_wholesale(
                filters={"name_or_company_name": data.name_or_company_name},
            )

            if exists:
                errors.append(
                    {
                        "loc": ("body", "name_or_company_name"),
                        "msg": CustomerWholesaleEntity.NAME_OR_COMPANY_NAME_IN_USE.value,
                        "type": "domain_validation",
                    }
                )

        # Validar que el número de teléfono no esté registrado en la base de datos
        if data.phone:
            exists = await self.__customer_wholesale_repo.exists_customer_wholesale(
                filters={"phone": data.phone},
            )

            if exists:
                errors.append(
                    {
                        "loc": ("body", "phone"),
                        "msg": CustomerWholesaleEntity.PHONE_IN_USE.value,
                        "type": "domain_validation",
                    }
                )

        # Validar que el número de documento no esté registrado en la base de datos
        if data.ruc:
            exists = await self.__customer_wholesale_repo.exists_customer_wholesale(
                filters={"ruc": data.ruc},
            )

            if exists:
                errors.append(
                    {
                        "loc": ("body", "ruc"),
                        "msg": CustomerWholesaleEntity.RUC_IN_USE.value,
                        "type": "domain_validation",
                    }
                )

        if errors:
            raise RequestValidationError(errors=errors)
