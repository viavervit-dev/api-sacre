from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.api.common.exceptions import DTOValidationErrorMessages
from src.api.modules.auth.constants import UserEntity
from src.api.modules.users.constants.customers import CUSTOMER_CONSTANTS, DocumentTypesCustomer


class CreateCustomerDTO(BaseModel):
    """Esquema de entrada para validar los datos requeridos en el registro de un nuevo cliente."""

    model_config = ConfigDict(use_enum_values=True)

    email: EmailStr = Field(
        max_length=UserEntity.EMAIL_MAX_LENGTH.value,
        description=UserEntity.EMAIL_DESCRIPTION.value,
        examples=["user@email.com"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR_EMAIL,
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
                DTOValidationErrorMessages.STRING_TOO_LONG,
                DTOValidationErrorMessages.STRING_TOO_SHORT,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
            ]
        },
    )
    first_names: str = Field(
        max_length=CUSTOMER_CONSTANTS.Limits.FIRST_NAMES_MAX_LENGTH,
        description=CUSTOMER_CONSTANTS.Docs.FIRST_NAMES_DESCRIPTION,
        examples=["Juan Pablo"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
            ]
        },
    )
    last_names: str = Field(
        max_length=CUSTOMER_CONSTANTS.Limits.LAST_NAMES_MAX_LENGTH,
        description=CUSTOMER_CONSTANTS.Docs.LAST_NAMES_DESCRIPTION,
        examples=["Pérez Gómez"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
            ]
        },
    )
    document_type: DocumentTypesCustomer = Field(
        description=CUSTOMER_CONSTANTS.Docs.DOCUMENT_TYPE_DESCRIPTION,
        examples=DocumentTypesCustomer.values(),
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
                DTOValidationErrorMessages.ENUM,
            ]
        },
    )
    document_number: str = Field(
        max_length=CUSTOMER_CONSTANTS.Limits.DOCUMENT_NUMBER_MAX_LENGTH,
        description=CUSTOMER_CONSTANTS.Docs.DOCUMENT_NUMBER_DESCRIPTION,
        examples=["12345678-9"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
                CUSTOMER_CONSTANTS.Errors.DOCUMENT_NUMBER_IN_USE,
            ]
        },
    )
    phone: str = Field(
        max_length=CUSTOMER_CONSTANTS.Limits.PHONE_MAX_LENGTH,
        description=CUSTOMER_CONSTANTS.Docs.PHONE_DESCRIPTION,
        examples=["+593 123456789"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
                CUSTOMER_CONSTANTS.Errors.PHONE_IN_USE,
            ]
        },
    )
