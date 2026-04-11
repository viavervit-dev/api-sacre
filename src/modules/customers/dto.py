from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.modules.authentication.constants import UserEntity
from src.modules.customers.constants import CustomerEntity, DocumentTypesCustomer


class CustomerCreateDTO(BaseModel):
    """DTO para la creación de un cliente"""

    email: EmailStr = Field(max_length=UserEntity.EMAIL_MAX_LENGTH.value)
    password: str = Field(
        max_length=UserEntity.PASSWORD_MAX_LENGTH.value,
        min_length=UserEntity.PASSWORD_MIN_LENGTH.value,
    )
    first_names: str = Field(max_length=CustomerEntity.FIRST_NAMES_MAX_LENGTH.value)
    last_names: str = Field(max_length=CustomerEntity.LAST_NAMES_MAX_LENGTH.value)
    document_number: str = Field(max_length=CustomerEntity.DOCUMENT_NUMBER_MAX_LENGTH.value)
    phone: str = Field(max_length=CustomerEntity.PHONE_MAX_LENGTH.value)
    document_type: str

    @field_validator("document_type")
    def document_type_must_be_allowed(cls, v: str) -> str:
        """Valida que el tipo de documento sea uno de los permitidos."""

        allowed = DocumentTypesCustomer.values()

        if v not in allowed:
            raise ValueError(CustomerEntity.DOCUMENT_TYPE_INVALID.value)

        return v


class CustomerReadDTO(BaseModel):
    """DTO para la lectura de un cliente"""

    id: UUID
    first_names: str
    last_names: str
    document_type: str
    document_number: str
    phone: str
