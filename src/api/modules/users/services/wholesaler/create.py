import secrets

from fastapi.exceptions import RequestValidationError

from src.api.modules.auth.constants import UserEntity, UserRoles
from src.api.modules.auth.repositories.interfaces import IUserRepository
from src.api.modules.users.constants import WholesalerEntity
from src.api.modules.users.dto import CreateWholesalerDTO, ReadWholesalerDTO
from src.api.modules.users.repositories.interfaces import IWholesalerRepository


class CreateWholesalerService:
    """Servicio encargado de la creación de clientes mayoristas."""

    def __init__(self, wholesaler_repo: IWholesalerRepository, user_repo: IUserRepository) -> None:
        self.__wholesaler_repo = wholesaler_repo
        self.__user_repo = user_repo

    async def create(self, data: CreateWholesalerDTO) -> ReadWholesalerDTO:
        """
        Registra un nuevo cliente mayorista tras validar las reglas de negocio del dominio.

        Raises:
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        # Ejecutar validaciones de las reglas de negocio
        await self.__run_business_validations(data=data)

        # Creamos el usuario base con su rol y permisos
        wholesaler_data = data.model_dump()
        wholesaler_data["products"] = []
        user_instance = await self.__user_repo.create_user(
            email=wholesaler_data.pop("email"),
            password=secrets.token_urlsafe(nbytes=12),
            role=UserRoles.CUSTOMER_WHOLESALE.value,
        )
        profile_instance = await self.__wholesaler_repo.create_wholesaler(
            user_id=user_instance.id,
            data=wholesaler_data,
        )
        user_instance.wholesaler = profile_instance

        # Instanciar el DTO de respuesta
        wholesaler_data = profile_instance.to_dict()
        wholesaler_data["id"] = user_instance.id
        wholesaler_data["email"] = user_instance.email

        return ReadWholesalerDTO.model_construct(**wholesaler_data)

    async def __run_business_validations(self, data: CreateWholesalerDTO) -> None:
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
            exists = await self.__wholesaler_repo.exists_wholesaler(
                filters={"name_or_company_name": data.name_or_company_name},
            )

            if exists:
                errors.append(
                    {
                        "loc": ("body", "name_or_company_name"),
                        "msg": WholesalerEntity.NAME_OR_COMPANY_NAME_IN_USE.value,
                        "type": "domain_validation",
                    }
                )

        # Validar que el número de teléfono no esté registrado en la base de datos
        if data.phone:
            exists = await self.__wholesaler_repo.exists_wholesaler(
                filters={"phone": data.phone},
            )

            if exists:
                errors.append(
                    {
                        "loc": ("body", "phone"),
                        "msg": WholesalerEntity.PHONE_IN_USE.value,
                        "type": "domain_validation",
                    }
                )

        # Validar que el número de documento no esté registrado en la base de datos
        if data.ruc:
            exists = await self.__wholesaler_repo.exists_wholesaler(
                filters={"ruc": data.ruc},
            )

            if exists:
                errors.append(
                    {
                        "loc": ("body", "ruc"),
                        "msg": WholesalerEntity.RUC_IN_USE.value,
                        "type": "domain_validation",
                    }
                )

        if errors:
            raise RequestValidationError(errors=errors)
