from typing import TypeVar
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from src.common.constants import DTOValidationErrorMessages
from src.modules.auth.constants import UserEntity

T = TypeVar("T")


class ReadUserDTO[T](BaseModel):
    """DTO para la lectura de datos de un usuario."""

    id: UUID = Field(
        description=UserEntity.ID_DESCRIPTION.value,
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    email: EmailStr = Field(
        description=UserEntity.EMAIL_DESCRIPTION.value,
        examples=["user@email.com"],
    )
    role_data: T = Field(
        description=UserEntity.ROLE_DATA_DESCRIPTION.value,
    )


class AdminCredentialsDTO(BaseModel):
    """DTO para las credenciales de autenticación de un administrador."""

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
    password: str = Field(
        description=UserEntity.PASSWORD_DESCRIPTION.value,
        examples=["6UjSV0QWmYfrFCG8"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.MISSING.value,
            ]
        },
    )


class CurrentUserDTO(BaseModel):
    """DTO para las credenciales de autenticación de un administrador."""

    first_names: str = Field(
        description=UserEntity.FIRST_NAME_DESCRIPTION.value,
        examples=["John Doe"],
    )
    last_names: str = Field(
        description=UserEntity.LAST_NAME_DESCRIPTION.value,
        examples=["John Doe"],
    )
    email: EmailStr = Field(
        description=UserEntity.EMAIL_DESCRIPTION.value,
        examples=["user@email.com"],
    )
    role: str = Field(
        description=UserEntity.ROLE_NAME_DESCRIPTION.value,
        examples=["admin", "customer"],
    )
