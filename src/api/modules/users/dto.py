from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from src.api.common.exceptions import DTOValidationErrorMessages
from src.api.modules.auth.constants import UserEntity
from src.api.modules.countries.dto import LocationEcuadorDTO, ReadLocationEcuadorDTO
from src.api.modules.users.constants import (
    CustomerEntity,
    DocumentTypesCustomer,
    WholesalerEntity,
)


class CreateCustomerDTO(BaseModel):
    """DTO para la creación de un cliente."""

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
        max_length=WholesalerEntity.POSITION_CONTACT_MAX_LENGTH.value,
        description=WholesalerEntity.POSITION_CONTACT_DESCRIPTION.value,
        examples=["Secretario"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                WholesalerEntity.NAME_OR_COMPANY_NAME_IN_USE.value,
            ]
        },
    )
    name: str = Field(
        max_length=WholesalerEntity.NAME_CONTACT_MAX_LENGTH.value,
        description=WholesalerEntity.NAME_CONTACT_DESCRIPTION.value,
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
        max_length=WholesalerEntity.PHONE_MAX_LENGTH.value,
        description=WholesalerEntity.PHONE_DESCRIPTION.value,
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
        description=WholesalerEntity.POSITION_CONTACT_DESCRIPTION.value,
        examples=["Secretario"],
    )
    name: str = Field(
        description=WholesalerEntity.NAME_CONTACT_DESCRIPTION.value,
        examples=["Juan Pablo"],
    )
    email: EmailStr = Field(
        description=UserEntity.EMAIL_DESCRIPTION.value,
        examples=["user@email.com"],
    )
    phone: str = Field(
        description=WholesalerEntity.PHONE_DESCRIPTION.value,
        examples=["+593 123456789"],
    )


class CreateWholesalerDTO(BaseModel):
    """DTO para la creación de un cliente mayorista."""

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
        max_length=WholesalerEntity.NAME_OR_COMPANY_NAME_MAX_LENGTH.value,
        description=WholesalerEntity.NAME_OR_COMPANY_NAME_DESCRIPTION.value,
        examples=["Juan Pablo", "Parroquia San José de Chaltura"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                WholesalerEntity.NAME_OR_COMPANY_NAME_IN_USE.value,
            ]
        },
    )
    ruc: str | None = Field(
        max_length=WholesalerEntity.RUC_MAX_LENGTH.value,
        description=WholesalerEntity.RUC_DESCRIPTION.value,
        examples=["1790011674001"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                WholesalerEntity.RUC_IN_USE.value,
            ]
        },
        default=None,
    )
    phone: str = Field(
        max_length=WholesalerEntity.PHONE_MAX_LENGTH.value,
        description=WholesalerEntity.PHONE_DESCRIPTION.value,
        examples=["+593 123456789"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                WholesalerEntity.PHONE_IN_USE.value,
            ]
        },
    )
    location: LocationEcuadorDTO = Field(
        description=WholesalerEntity.LOCATION_DESCRIPTION.value,
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )
    extra_contacts: list[ExtraContactsDTO] | None = Field(
        description=WholesalerEntity.EXTRA_CONTACTS_DESCRIPTION.value,
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
        default=None,
    )


class UpdateWholesalerDTO(BaseModel):
    """DTO para la actualización de un cliente mayorista."""

    name_or_company_name: str | None = Field(
        max_length=WholesalerEntity.NAME_OR_COMPANY_NAME_MAX_LENGTH.value,
        description=WholesalerEntity.NAME_OR_COMPANY_NAME_DESCRIPTION.value,
        examples=["Juan Pablo", "Parroquia San José de Chaltura"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                WholesalerEntity.NAME_OR_COMPANY_NAME_IN_USE.value,
            ]
        },
        default=None,
    )
    ruc: str | None = Field(
        max_length=WholesalerEntity.RUC_MAX_LENGTH.value,
        description=WholesalerEntity.RUC_DESCRIPTION.value,
        examples=["1790011674001"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                WholesalerEntity.RUC_IN_USE.value,
            ]
        },
        default=None,
    )
    phone: str | None = Field(
        max_length=WholesalerEntity.PHONE_MAX_LENGTH.value,
        description=WholesalerEntity.PHONE_DESCRIPTION.value,
        examples=["+593 123456789"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                WholesalerEntity.PHONE_IN_USE.value,
            ]
        },
        default=None,
    )
    location: LocationEcuadorDTO | None = Field(
        description=WholesalerEntity.LOCATION_DESCRIPTION.value,
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
        default=None,
    )
    extra_contacts: list[ExtraContactsDTO] | None = Field(
        description=WholesalerEntity.EXTRA_CONTACTS_DESCRIPTION.value,
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
        default=None,
    )


class ReadWholesalerDTO(BaseModel):
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
        description=WholesalerEntity.NAME_OR_COMPANY_NAME_DESCRIPTION.value,
        examples=["Juan Pablo", "Parroquia San José de Chaltura"],
    )
    products: list[UUID] = Field(
        description=WholesalerEntity.PRODUCTS_DESCRIPTION.value,
        examples=[["3fa85f64-5717-4562-b3fc-2c963f66afa6"], []],
    )
    ruc: str | None = Field(
        description=WholesalerEntity.RUC_DESCRIPTION.value,
        examples=["1790011674001"],
    )
    phone: str = Field(
        description=WholesalerEntity.PHONE_DESCRIPTION.value,
        examples=["+593 123456789"],
    )
    location: ReadLocationEcuadorDTO = Field(
        description=WholesalerEntity.LOCATION_DESCRIPTION.value
    )
    extra_contacts: list[ReadExtraContactsDTO] | None = Field(
        description=WholesalerEntity.EXTRA_CONTACTS_DESCRIPTION.value,
    )


class ReadWholesalerSummaryDTO(BaseModel):
    """DTO de lectura resumida de un cliente mayorista en listados paginados."""

    id: UUID = Field(
        description="Identificador único (UUID v4).",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    name_or_company_name: str = Field(
        description=WholesalerEntity.NAME_OR_COMPANY_NAME_DESCRIPTION.value,
        examples=["Juan Pablo", "Parroquia San José de Chaltura"],
    )
    location: ReadLocationEcuadorDTO = Field(
        description=WholesalerEntity.LOCATION_DESCRIPTION.value
    )
    date_joined: datetime = Field(
        description="Fecha y hora de creación de la orden/transacción.",
        examples=["2026-10-24T17:25:41.776689+00:00"],
    )
