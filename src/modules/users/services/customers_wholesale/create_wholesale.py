from typing import Any

from fastapi.exceptions import RequestValidationError

from src.modules.auth.constants import UserEntity
from src.modules.users.constants import WholesaleEntity
from src.modules.users.dto import CreateCustomerWholesaleDTO, ReadCustomerWholesaleDTO
from src.modules.users.repositories.interfaces import ICustomerWholesaleRepository


class CreateCustomerWholesaleService:
    """Servicio encargado de la validación de negocio y registro de clientes mayoristas."""

    def __init__(self, customer_wholesale_repo: ICustomerWholesaleRepository) -> None:
        self.__customer_wholesale_repo = customer_wholesale_repo

    async def create_customer_wholesale(
        self,
        data: CreateCustomerWholesaleDTO,
    ) -> ReadCustomerWholesaleDTO:
        """
        Registra un nuevo cliente mayorista tras validar las reglas de negocio del dominio.

        Raises:
            RequestValidationError: Si falla alguna validacion de negocio.
        """

        # Validaciones de negocio
        wholesale_data = data.model_dump()
        await self.__run_business_validations(data=wholesale_data)

        # Creamos el usuario
        wholesale_instance = await self.__customer_wholesale_repo.create_customer_wholesale(
            data=wholesale_data
        )

        return ReadCustomerWholesaleDTO.model_construct(
            id=wholesale_instance.id,
            email=wholesale_instance.email,
            name_or_company_name=wholesale_instance.name_or_company_name,
            ruc=wholesale_instance.ruc,
            phone=wholesale_instance.phone,
            location=wholesale_instance.location,
            extra_contacts=wholesale_instance.extra_contacts,
        )

    async def __run_business_validations(self, data: dict[str, Any]) -> None:
        """
        Ejecuta las validaciones de negocio previas al registro del cliente mayorista.

        Raises:
            RequestValidationError: Si falla alguna validacion de negocio.
        """

        errors = []

        # Validar que el correo electrónico no esté registrado en la base de datos
        exists = await self.__customer_wholesale_repo.exists_customer_wholesale(
            filters={"email": data["email"]}
        )

        if exists:
            errors.append(
                {
                    "loc": ("body", "email"),
                    "msg": UserEntity.EMAIL_IN_USE.value,
                    "type": "domain_validation",
                }
            )

        # Validar que el nombre o razón social no esté registrado en la base de datos
        exists = await self.__customer_wholesale_repo.exists_customer_wholesale(
            filters={"name_or_company_name": data["name_or_company_name"]}
        )

        if exists:
            errors.append(
                {
                    "loc": ("body", "name_or_company_name"),
                    "msg": WholesaleEntity.NAME_OR_COMPANY_NAME_IN_USE.value,
                    "type": "domain_validation",
                }
            )

        # Validar que el número de teléfono no esté registrado en la base de datos
        exists = await self.__customer_wholesale_repo.exists_customer_wholesale(
            filters={"phone": data["phone"]}
        )

        if exists:
            errors.append(
                {
                    "loc": ("body", "phone"),
                    "msg": WholesaleEntity.PHONE_IN_USE.value,
                    "type": "domain_validation",
                }
            )

        # Validar que el número de documento no esté registrado en la base de datos
        exists = await self.__customer_wholesale_repo.exists_customer_wholesale(
            filters={"ruc": data["ruc"]},
        )

        if exists:
            errors.append(
                {
                    "loc": ("body", "ruc"),
                    "msg": WholesaleEntity.RUC_IN_USE.value,
                    "type": "domain_validation",
                }
            )

        if errors:
            raise RequestValidationError(errors=errors)
