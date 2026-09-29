from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.common.constants import DTOValidationErrorMessages
from src.modules.auth.constants import UserEntity
from src.modules.users.constants import (
    CustomerEntity,
    DocumentTypesCustomer,
    Ecuador,
    WholesaleEntity,
)


class CreateCustomerDTO(BaseModel):
    """DTO para el registro y creación de un cliente."""

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
                CustomerEntity.PHONE_IN_USE.value,
            ]
        },
    )


class ExtraContactsDTO(BaseModel):
    """DTO para la información de un contacto adicional o secundario."""

    position: str = Field(
        max_length=WholesaleEntity.POSITION_CONTACT_MAX_LENGTH.value,
        description=WholesaleEntity.POSITION_CONTACT_DESCRIPTION.value,
        examples=["Secretario"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                WholesaleEntity.NAME_OR_COMPANY_NAME_IN_USE.value,
            ]
        },
    )
    name: str = Field(
        max_length=WholesaleEntity.NAME_CONTACT_MAX_LENGTH.value,
        description=WholesaleEntity.NAME_CONTACT_DESCRIPTION.value,
        examples=["Juan Pablo"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )
    email: EmailStr = Field(
        max_length=UserEntity.EMAIL_MAX_LENGTH.value,
        description=UserEntity.EMAIL_DESCRIPTION.value,
        examples=["user@email.com"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR_EMAIL.value,
            ]
        },
    )
    phone: str = Field(
        max_length=WholesaleEntity.PHONE_MAX_LENGTH.value,
        description=WholesaleEntity.PHONE_DESCRIPTION.value,
        examples=["+593 123456789"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )


class ReadExtraContactsDTO(BaseModel):
    """DTO de lectura para la información de un contacto adicional o secundario."""

    position: str = Field(
        description=WholesaleEntity.POSITION_CONTACT_DESCRIPTION.value,
        examples=["Secretario"],
    )
    name: str = Field(
        description=WholesaleEntity.NAME_CONTACT_DESCRIPTION.value,
        examples=["Juan Pablo"],
    )
    email: EmailStr = Field(
        description=UserEntity.EMAIL_DESCRIPTION.value,
        examples=["user@email.com"],
    )
    phone: str = Field(
        description=WholesaleEntity.PHONE_DESCRIPTION.value,
        examples=["+593 123456789"],
    )


class LocationDTO(BaseModel):
    """DTO para los datos de ubicación geográfica y dirección."""

    model_config = ConfigDict(use_enum_values=True)

    country: Ecuador = Field(
        description="Nombre del país.",
        examples=Ecuador.values(),
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.ENUM.value,
            ]
        },
    )
    province: str = Field(
        max_length=100,
        description="Nombre oficial de la provincia.",
        examples=["Juan Pablo"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )
    canton: EmailStr = Field(
        max_length=100,
        description="Nombre oficial del cantón.",
        examples=["user@email.com"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR_EMAIL.value,
            ]
        },
    )
    city: str = Field(
        max_length=100,
        description="Nombre oficial de la ciudad o localidad.",
        examples=["+593 123456789"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )
    address: str = Field(
        max_length=100,
        description="Dirección de entrega.",
        examples=["Manzana 12 casa 32"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )


class ReadLocationDTO(BaseModel):
    """DTO de lectura para los datos de ubicación geográfica y dirección."""

    model_config = ConfigDict(use_enum_values=True)

    country: Ecuador = Field(
        description="Nombre del país.",
        examples=Ecuador.values(),
    )
    province: str = Field(
        description="Nombre oficial de la provincia.",
        examples=["Juan Pablo"],
    )
    canton: EmailStr = Field(
        description="Nombre oficial del cantón.",
        examples=["user@email.com"],
    )
    city: str = Field(
        description="Nombre oficial de la ciudad o localidad.",
        examples=["+593 123456789"],
    )
    address: str = Field(
        description="Dirección de entrega.",
        examples=["Manzana 12 casa 32"],
    )


class CreateCustomerWholesaleDTO(BaseModel):
    """DTO para el registro de un cliente mayorista."""

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
    name_or_company_name: str = Field(
        max_length=WholesaleEntity.NAME_OR_COMPANY_NAME_MAX_LENGTH.value,
        description=WholesaleEntity.NAME_OR_COMPANY_NAME_DESCRIPTION.value,
        examples=["Juan Pablo", "Parroquia San José de Chaltura"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                WholesaleEntity.NAME_OR_COMPANY_NAME_IN_USE.value,
            ]
        },
    )
    ruc: str | None = Field(
        max_length=WholesaleEntity.RUC_MAX_LENGTH.value,
        description=WholesaleEntity.RUC_DESCRIPTION.value,
        examples=["1790011674001"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                WholesaleEntity.RUC_IN_USE.value,
            ]
        },
        default=None,
    )
    phone: str = Field(
        max_length=WholesaleEntity.PHONE_MAX_LENGTH.value,
        description=WholesaleEntity.PHONE_DESCRIPTION.value,
        examples=["+593 123456789"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                WholesaleEntity.PHONE_IN_USE.value,
            ]
        },
    )
    location: LocationDTO = Field(description=WholesaleEntity.LOCATION_DESCRIPTION.value)
    extra_contacts: list[ExtraContactsDTO] | None = Field(
        description=WholesaleEntity.EXTRA_CONTACTS_DESCRIPTION.value,
        default=None,
    )


class ReadCustomerWholesaleDTO(BaseModel):
    """DTO de lectura para el registro de un cliente mayorista."""

    id: UUID = Field(
        description="Identificador único (UUID v4).",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    email: str = Field(
        description=UserEntity.EMAIL_DESCRIPTION.value,
        examples=["user@email.com"],
    )
    name_or_company_name: str = Field(
        description=WholesaleEntity.NAME_OR_COMPANY_NAME_DESCRIPTION.value,
        examples=["Juan Pablo", "Parroquia San José de Chaltura"],
    )
    ruc: str | None = Field(
        description=WholesaleEntity.RUC_DESCRIPTION.value,
        examples=["1790011674001"],
    )
    phone: str = Field(
        description=WholesaleEntity.PHONE_DESCRIPTION.value,
        examples=["+593 123456789"],
    )
    location: ReadLocationDTO = Field(description=WholesaleEntity.LOCATION_DESCRIPTION.value)
    extra_contacts: list[ReadExtraContactsDTO] | None = Field(
        description=WholesaleEntity.EXTRA_CONTACTS_DESCRIPTION.value,
    )
