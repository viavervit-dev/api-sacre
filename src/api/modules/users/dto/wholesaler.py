from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from src.api.common.exceptions import DTOValidationErrorMessages
from src.api.modules.auth.constants import UserEntity
from src.api.modules.countries.dto import LocationEcuadorDTO, ReadLocationEcuadorDTO
from src.api.modules.users.constants.wholesaler import WHOLESALER_CONSTANTS


class ExtraContactsDTO(BaseModel):
    """Esquema de entrada para validar los datos de un contacto secundario del mayorista."""

    position: str = Field(
        max_length=WHOLESALER_CONSTANTS.Limits.POSITION_CONTACT_MAX_LENGTH,
        description=WHOLESALER_CONSTANTS.Docs.POSITION_CONTACT_DESCRIPTION,
        examples=["Secretario"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
                WHOLESALER_CONSTANTS.Errors.NAME_OR_COMPANY_NAME_IN_USE,
            ]
        },
    )
    name: str = Field(
        max_length=WHOLESALER_CONSTANTS.Limits.NAME_CONTACT_MAX_LENGTH,
        description=WHOLESALER_CONSTANTS.Docs.NAME_CONTACT_DESCRIPTION,
        examples=["Juan Pablo"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
            ]
        },
    )
    email: EmailStr = Field(
        max_length=UserEntity.EMAIL_MAX_LENGTH.value,
        description=UserEntity.EMAIL_DESCRIPTION.value,
        examples=["user@email.com"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR_EMAIL,
            ]
        },
    )
    phone: str = Field(
        max_length=WHOLESALER_CONSTANTS.Limits.PHONE_MAX_LENGTH,
        description=WHOLESALER_CONSTANTS.Docs.PHONE_DESCRIPTION,
        examples=["+593 123456789"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
            ]
        },
    )


class ReadExtraContactsDTO(BaseModel):
    """Esquema de salida con los datos de un contacto secundario del mayorista."""

    position: str = Field(
        description=WHOLESALER_CONSTANTS.Docs.POSITION_CONTACT_DESCRIPTION,
        examples=["Secretario"],
    )
    name: str = Field(
        description=WHOLESALER_CONSTANTS.Docs.NAME_CONTACT_DESCRIPTION,
        examples=["Juan Pablo"],
    )
    email: EmailStr = Field(
        description=UserEntity.EMAIL_DESCRIPTION.value,
        examples=["user@email.com"],
    )
    phone: str = Field(
        description=WHOLESALER_CONSTANTS.Docs.PHONE_DESCRIPTION,
        examples=["+593 123456789"],
    )


class CreateWholesalerDTO(BaseModel):
    """
    Esquema de entrada para validar los datos requeridos en el registro de un cliente mayorista.
    """

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
    name_or_company_name: str = Field(
        max_length=WHOLESALER_CONSTANTS.Limits.NAME_OR_COMPANY_NAME_MAX_LENGTH,
        description=WHOLESALER_CONSTANTS.Docs.NAME_OR_COMPANY_NAME_DESCRIPTION,
        examples=["Juan Pablo", "Parroquia San José de Chaltura"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
                WHOLESALER_CONSTANTS.Errors.NAME_OR_COMPANY_NAME_IN_USE,
            ]
        },
    )
    ruc: str | None = Field(
        max_length=WHOLESALER_CONSTANTS.Limits.RUC_MAX_LENGTH,
        description=WHOLESALER_CONSTANTS.Docs.RUC_DESCRIPTION,
        examples=["1790011674001"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG,
                DTOValidationErrorMessages.VALUE_ERROR,
                WHOLESALER_CONSTANTS.Errors.RUC_IN_USE,
            ]
        },
        default=None,
    )
    phone: str = Field(
        max_length=WHOLESALER_CONSTANTS.Limits.PHONE_MAX_LENGTH,
        description=WHOLESALER_CONSTANTS.Docs.PHONE_DESCRIPTION,
        examples=["+593 123456789"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
                WHOLESALER_CONSTANTS.Errors.PHONE_IN_USE,
            ]
        },
    )
    location: LocationEcuadorDTO = Field(
        description=WHOLESALER_CONSTANTS.Docs.LOCATION_DESCRIPTION,
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
            ]
        },
    )
    extra_contacts: list[ExtraContactsDTO] | None = Field(
        description=WHOLESALER_CONSTANTS.Docs.EXTRA_CONTACTS_DESCRIPTION,
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
            ]
        },
        default=None,
    )


class UpdateWholesalerDTO(BaseModel):
    """
    Esquema de entrada para validar actualizaciones parciales de la información de un
    cliente mayorista.
    """

    name_or_company_name: str | None = Field(
        max_length=WHOLESALER_CONSTANTS.Limits.NAME_OR_COMPANY_NAME_MAX_LENGTH,
        description=WHOLESALER_CONSTANTS.Docs.NAME_OR_COMPANY_NAME_DESCRIPTION,
        examples=["Juan Pablo", "Parroquia San José de Chaltura"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
                WHOLESALER_CONSTANTS.Errors.NAME_OR_COMPANY_NAME_IN_USE,
            ]
        },
        default=None,
    )
    ruc: str | None = Field(
        max_length=WHOLESALER_CONSTANTS.Limits.RUC_MAX_LENGTH,
        description=WHOLESALER_CONSTANTS.Docs.RUC_DESCRIPTION,
        examples=["1790011674001"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG,
                DTOValidationErrorMessages.VALUE_ERROR,
                WHOLESALER_CONSTANTS.Errors.RUC_IN_USE,
            ]
        },
        default=None,
    )
    phone: str | None = Field(
        max_length=WHOLESALER_CONSTANTS.Limits.PHONE_MAX_LENGTH,
        description=WHOLESALER_CONSTANTS.Docs.PHONE_DESCRIPTION,
        examples=["+593 123456789"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
                WHOLESALER_CONSTANTS.Errors.PHONE_IN_USE,
            ]
        },
        default=None,
    )
    location: LocationEcuadorDTO | None = Field(
        description=WHOLESALER_CONSTANTS.Docs.LOCATION_DESCRIPTION,
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
            ]
        },
        default=None,
    )
    extra_contacts: list[ExtraContactsDTO] | None = Field(
        description=WHOLESALER_CONSTANTS.Docs.EXTRA_CONTACTS_DESCRIPTION,
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
            ]
        },
        default=None,
    )


class ReadWholesalerDTO(BaseModel):
    """Esquema de salida con el detalle completo de un cliente mayorista."""

    id: UUID = Field(
        description="Identificador único (UUID v4).",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    email: str = Field(
        description=UserEntity.EMAIL_DESCRIPTION.value,
        examples=["user@email.com"],
    )
    name_or_company_name: str = Field(
        description=WHOLESALER_CONSTANTS.Docs.NAME_OR_COMPANY_NAME_DESCRIPTION,
        examples=["Juan Pablo", "Parroquia San José de Chaltura"],
    )
    products: list[UUID] = Field(
        description=WHOLESALER_CONSTANTS.Docs.PRODUCTS_DESCRIPTION,
        examples=[["3fa85f64-5717-4562-b3fc-2c963f66afa6"], []],
    )
    ruc: str | None = Field(
        description=WHOLESALER_CONSTANTS.Docs.RUC_DESCRIPTION,
        examples=["1790011674001"],
    )
    phone: str = Field(
        description=WHOLESALER_CONSTANTS.Docs.PHONE_DESCRIPTION,
        examples=["+593 123456789"],
    )
    location: ReadLocationEcuadorDTO = Field(
        description=WHOLESALER_CONSTANTS.Docs.LOCATION_DESCRIPTION
    )
    extra_contacts: list[ReadExtraContactsDTO] | None = Field(
        description=WHOLESALER_CONSTANTS.Docs.EXTRA_CONTACTS_DESCRIPTION,
    )


class ReadWholesalerSummaryDTO(BaseModel):
    """Esquema de salida con la información resumida de un cliente mayorista para listados."""

    id: UUID = Field(
        description="Identificador único (UUID v4).",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    name_or_company_name: str = Field(
        description=WHOLESALER_CONSTANTS.Docs.NAME_OR_COMPANY_NAME_DESCRIPTION,
        examples=["Juan Pablo", "Parroquia San José de Chaltura"],
    )
    location: ReadLocationEcuadorDTO = Field(
        description=WHOLESALER_CONSTANTS.Docs.LOCATION_DESCRIPTION
    )
    date_joined: datetime = Field(
        description="Fecha y hora de creación de la orden/transacción.",
        examples=["2026-10-24T17:25:41.776689+00:00"],
    )
