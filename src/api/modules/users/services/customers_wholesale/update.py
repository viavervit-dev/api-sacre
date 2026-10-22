from uuid import UUID

from fastapi.exceptions import RequestValidationError

from src.api.common.exceptions import ResourceNotFound
from src.api.modules.auth.constants import UserRoles
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

    async def update(
        self,
        data: UpdateCustomerWholesaleDTO,
        customer_wholesale_id: UUID,
    ) -> ReadCustomerWholesaleDTO:
        """
        Actualiza un cliente mayorista tras validar las reglas de negocio del dominio.

        Raises:
            ResourceNotFound: Si el cliente mayorista no existe en la base de datos.
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        # Validar que el cliente mayorista exista en la base de datos
        user_instance = await self.__user_repo.get_user(
            filters={
                "role": UserRoles.CUSTOMER_WHOLESALE.value,
                "id": customer_wholesale_id,
            },
            load_permissions=False,
        )

        if not user_instance:
            raise ResourceNotFound()

        # Se ejecutan validaciones de negocio
        await self.__run_business_validations(data=data)

        # Actualizar el producto en la base de datos
        customer_wholesale_data = data.model_dump(exclude_none=True)
        profile_instance = await self.__customer_wholesale_repo.update_customer_wholesale(
            instance=user_instance.customer_wholesale,
            data=customer_wholesale_data,
        )

        # Instanciar el DTO de respuesta
        customer_wholesale_data = profile_instance.to_dict()
        customer_wholesale_data["id"] = user_instance.id
        customer_wholesale_data["email"] = user_instance.email

        return ReadCustomerWholesaleDTO.model_construct(**customer_wholesale_data)

    async def __run_business_validations(self, data: UpdateCustomerWholesaleDTO) -> None:
        """
        Ejecuta las validaciones de negocio previas a la actualización del cliente mayorista.

        Raises:
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        errors = []

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
