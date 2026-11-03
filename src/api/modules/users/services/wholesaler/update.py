from uuid import UUID

from fastapi.exceptions import RequestValidationError

from src.api.common.exceptions import ResourceNotFound
from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.repositories.interfaces import IUserRepository
from src.api.modules.users.constants import WholesalerEntity
from src.api.modules.users.dto import ReadWholesalerDTO, UpdateWholesalerDTO
from src.api.modules.users.repositories.interfaces import IWholesalerRepository


class UpdateWholesalerService:
    """Servicio encargado de la actualización de clientes mayoristas."""

    def __init__(self, wholesaler_repo: IWholesalerRepository, user_repo: IUserRepository) -> None:
        self.__wholesaler_repo = wholesaler_repo
        self.__user_repo = user_repo

    async def update(self, data: UpdateWholesalerDTO, wholesaler_id: UUID) -> ReadWholesalerDTO:
        """
        Actualiza un cliente mayorista tras validar las reglas de negocio del dominio.

        Raises:
            ResourceNotFound: Si el cliente mayorista no existe en la base de datos.
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        # Validar que el cliente mayorista exista en la base de datos
        user_instance = await self.__user_repo.get_user(
            filters={"role": UserRoles.WHOLESALER.value, "id": wholesaler_id},
            load_permissions=False,
        )

        if not user_instance:
            raise ResourceNotFound()

        # Se ejecutan validaciones de negocio
        await self.__run_business_validations(data=data)

        # Actualizar el producto en la base de datos
        wholesaler_data = data.model_dump(exclude_none=True)
        profile_instance = await self.__wholesaler_repo.update_wholesaler(
            instance=user_instance.wholesaler,
            data=wholesaler_data,
        )

        # Instanciar el DTO de respuesta
        wholesaler_data = profile_instance.to_dict()
        wholesaler_data["id"] = user_instance.id
        wholesaler_data["email"] = user_instance.email

        return ReadWholesalerDTO.model_construct(**wholesaler_data)

    async def __run_business_validations(self, data: UpdateWholesalerDTO) -> None:
        """
        Ejecuta las validaciones de negocio previas a la actualización del cliente mayorista.

        Raises:
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        errors = []

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
