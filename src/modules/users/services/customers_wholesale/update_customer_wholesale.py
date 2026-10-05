from typing import Any
from uuid import UUID

from fastapi.exceptions import RequestValidationError

from src.common.exceptions import ResourceNotFound
from src.modules.auth.constants import UserEntity
from src.modules.users.constants import CustomerWholesaleEntity
from src.modules.users.dto import ReadCustomerWholesaleDTO, UpdateCustomerWholesaleDTO
from src.modules.users.repositories.interfaces import ICustomerWholesaleRepository


class UpdateCustomerWholesaleService:
    """Servicio encargado de la validación de negocio y actualización de clientes mayoristas."""

    def __init__(self, customer_wholesale_repo: ICustomerWholesaleRepository) -> None:
        self.__customer_wholesale_repo = customer_wholesale_repo

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

        customer_wholesale_data = data.model_dump(exclude_unset=True)
        instance = await self.__customer_wholesale_repo.get_customer_wholesale(id=id)

        if not instance:
            raise ResourceNotFound()

        await self.__run_business_validations(data=customer_wholesale_data)

        # Actualizar el producto en la base de datos
        instance = await self.__customer_wholesale_repo.update_customer_wholesale(
            data=customer_wholesale_data,
            instance=instance,
        )

        return ReadCustomerWholesaleDTO.model_construct(
            id=instance.id,
            email=instance.email,
            name_or_company_name=instance.name_or_company_name,
            ruc=instance.ruc,
            phone=instance.phone,
            location=instance.location,
            extra_contacts=instance.extra_contacts,
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
