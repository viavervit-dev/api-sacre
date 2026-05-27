from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.constants import DTOValidationErrorMessages
from src.modules.auth.constants import UserEntity, UserRoles
from src.modules.auth.repositories.interfaces import IUserRepository
from src.modules.customers.constants import CustomerEntity, DocumentTypesCustomer


class CreateCustomerDTO(BaseModel):
    """DTO para la creación de un cliente."""

    model_config = ConfigDict(use_enum_values=True)

    email: EmailStr = Field(
        max_length=UserEntity.EMAIL_MAX_LENGTH.value,
        description=UserEntity.EMAIL_DESCRIPTION.value,
        examples=["user@email.com"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR_EMAIL.value,
                UserEntity.EMAIL_IN_USE.value,
            ]
        },
    )
    password: str = Field(
        max_length=UserEntity.PASSWORD_MAX_LENGTH.value,
        min_length=UserEntity.PASSWORD_MIN_LENGTH.value,
        description=UserEntity.PASSWORD_DESCRIPTION.value,
        examples=["6UjSV0QWmYfrFCG8"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.STRING_TOO_SHORT.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )
    first_names: str = Field(
        max_length=CustomerEntity.FIRST_NAMES_MAX_LENGTH.value,
        description=CustomerEntity.FIRST_NAMES_DESCRIPTION.value,
        examples=["Juan Pablo"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )
    last_names: str = Field(
        max_length=CustomerEntity.LAST_NAMES_MAX_LENGTH.value,
        description=CustomerEntity.LAST_NAMES_DESCRIPTION.value,
        examples=["Pérez Gómez"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )
    document_type: DocumentTypesCustomer = Field(
        description=CustomerEntity.DOCUMENT_TYPE_DESCRIPTION.value,
        examples=DocumentTypesCustomer.values(),
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.ENUM.value,
            ]
        },
    )
    document_number: str = Field(
        max_length=CustomerEntity.DOCUMENT_NUMBER_MAX_LENGTH.value,
        description=CustomerEntity.DOCUMENT_NUMBER_DESCRIPTION.value,
        examples=["12345678-9"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                CustomerEntity.DOCUMENT_NUMBER_IN_USE.value,
            ]
        },
    )
    phone: str = Field(
        max_length=CustomerEntity.PHONE_MAX_LENGTH.value,
        description=CustomerEntity.PHONE_DESCRIPTION.value,
        examples=["+593 123456789"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                CustomerEntity.DOCUMENT_NUMBER_IN_USE.value,
            ]
        },
    )

    async def check_email(
        self,
        db: AsyncSession,
        user_repo: type[IUserRepository],
    ) -> None:
        """Ejecuta validaciones para el correo electrónico del cliente."""

        # Validar que el correo electrónico no esté registrado en la base de datos
        exists = await user_repo.exists_user(
            filters={"email": self.email},
            role=UserRoles.CUSTOMER.value,
            db=db,
        )

        if exists:
            raise RequestValidationError(
                errors=[
                    {
                        "loc": ("body", "email"),
                        "msg": UserEntity.EMAIL_IN_USE.value,
                        "type": "domain_validation",
                    }
                ]
            )

    async def check_phone(
        self,
        db: AsyncSession,
        user_repo: type[IUserRepository],
    ) -> None:
        """Ejecuta validaciones para el número de teléfono del cliente."""

        # Validar que el número de teléfono no esté registrado en la base de datos
        exists = await user_repo.exists_user(
            filters={"phone": self.phone},
            role=UserRoles.CUSTOMER.value,
            db=db,
        )

        if exists:
            raise RequestValidationError(
                errors=[
                    {
                        "loc": ("body", "phone"),
                        "msg": CustomerEntity.PHONE_IN_USE.value,
                        "type": "domain_validation",
                    }
                ]
            )

    async def check_document_number(
        self,
        db: AsyncSession,
        user_repo: type[IUserRepository],
    ) -> None:
        """Ejecuta validaciones para el número de documento del cliente."""

        # Validar que el número de documento no esté registrado en la base de datos
        exists = await user_repo.exists_user(
            filters={"document_number": self.document_number},
            role=UserRoles.CUSTOMER.value,
            db=db,
        )

        if exists:
            raise RequestValidationError(
                errors=[
                    {
                        "loc": ("body", "document_number"),
                        "msg": CustomerEntity.DOCUMENT_NUMBER_IN_USE.value,
                        "type": "domain_validation",
                    }
                ]
            )


class ReadCustomerDTO(BaseModel):
    """DTO para la lectura de datos de un cliente"""

    first_names: str = Field(
        description=CustomerEntity.FIRST_NAMES_DESCRIPTION.value,
        examples=["Juan Pablo"],
    )
    last_names: str = Field(
        description=CustomerEntity.LAST_NAMES_DESCRIPTION.value,
        examples=["Pérez Gómez"],
    )
    document_type: str = Field(
        description=CustomerEntity.DOCUMENT_TYPE_DESCRIPTION.value,
        examples=DocumentTypesCustomer.values(),
    )
    document_number: str = Field(
        description=CustomerEntity.DOCUMENT_NUMBER_DESCRIPTION.value,
        examples=["12345678-9"],
    )
    phone: str = Field(
        description=CustomerEntity.PHONE_DESCRIPTION.value,
        examples=["+593 123456789"],
    )
