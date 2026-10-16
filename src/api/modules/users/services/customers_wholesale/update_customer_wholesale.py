from typing import Any
from uuid import UUID

from fastapi.exceptions import RequestValidationError

from src.api.common.exceptions import ResourceNotFound
from src.api.modules.auth.constants import UserEntity, UserRoles
from src.api.modules.auth.repositories.interfaces import IUserRepository
from src.api.modules.users.constants import CustomerWholesaleEntity
from src.api.modules.users.dto import ReadCustomerWholesaleDTO, UpdateCustomerWholesaleDTO
from src.api.modules.users.repositories.interfaces import ICustomerWholesaleRepository


class UpdateCustomerWholesaleService:
    """Servicio encargado de la validación de negocio y actualización de clientes mayoristas."""

    def __init__(
        self,
        customer_wholesale_repo: ICustomerWholesaleRepository,
        user_repo: IUserRepository,
    ) -> None:
        self.__customer_wholesale_repo = customer_wholesale_repo
        self.__user_repo = user_repo

    async def update_customer_wholesale(
        self,
        data: UpdateCustomerWholesaleDTO,
        id: UUID,
    ) -> ReadCustomerWholesaleDTO:
        """
        Actualiza un cliente mayorista tras validar las reglas de negocio del dominio.

        Raises:
            ResourceNotFound: Si el cliente mayorista no existe en la base de datos.
            RequestValidationError: Si falla alguna regla de validación de negocio.
        """

        # Validar que el cliente mayorista exista en la base de datos
        user = await self.__user_repo.get_user(
            filters={
                "role": UserRoles.CUSTOMER_WHOLESALE.value,
                "id": id,
            },
            load_permissions=False,
        )

        if not user:
            raise ResourceNotFound()

        # Se ejecutan validaciones de negocio
        user_data = data.model_dump()
        await self.__run_business_validations(data=user_data)

        # Actualizar el producto en la base de datos
        profile = await self.__customer_wholesale_repo.update_customer_wholesale(
            instance=user.customer_wholesale,
            data=user_data,
        )

        return ReadCustomerWholesaleDTO.model_construct(
            id=user.id,
            email=user.email,
            name_or_company_name=profile.name_or_company_name,
            ruc=profile.ruc,
            phone=profile.phone,
            location=profile.location,
            extra_contacts=profile.extra_contacts,
        )

    async def __run_business_validations(self, data: dict[str, Any]) -> None:
        """
        Ejecuta las validaciones de negocio previas a la actualización del cliente mayorista.

        Raises:
            RequestValidationError: Si alguno de los campos únicos a actualizar ya está en uso.
        """

        errors = []

        # Validar que el correo electrónico no esté registrado en la base de datos
        if data.get("email"):
            exists = await self.__user_repo.exists_user(filters={"email": data["email"]})

            if exists:
                errors.append(
                    {
                        "loc": ("body", "email"),
                        "msg": UserEntity.EMAIL_IN_USE.value,
                        "type": "domain_validation",
                    }
                )

        # Validar que el nombre o razón social no esté registrado en la base de datos
        if data.get("name_or_company_name"):
            exists = await self.__customer_wholesale_repo.exists_customer_wholesale(
                filters={"name_or_company_name": data["name_or_company_name"]}
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
        if data.get("phone"):
            exists = await self.__customer_wholesale_repo.exists_customer_wholesale(
                filters={"phone": data["phone"]}
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
        if data.get("ruc"):
            exists = await self.__customer_wholesale_repo.exists_customer_wholesale(
                filters={"ruc": data["ruc"]},
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
