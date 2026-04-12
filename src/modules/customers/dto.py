from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.authentication.constants import UserEntity
from src.modules.customers.constants import CustomerEntity, DocumentTypesCustomer
from src.modules.customers.repositories.interfaces import ICustomerRepository


class CreateCustomerDTO(BaseModel):
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
    def document_type_must_be_allowed(self, v: str) -> str:
        """Valida que el tipo de documento sea uno de los permitidos."""

        allowed = DocumentTypesCustomer.values()

        if v not in allowed:
            raise ValueError(CustomerEntity.DOCUMENT_TYPE_INVALID.value)

        return v

    async def check_email(self, session: AsyncSession, repository: ICustomerRepository) -> None:
        """Ejecuta validaciones para el correo electrónico del cliente."""

        # Validar que el correo electrónico no esté registrado en la base de datos
        email_exists = await repository.exists(session, email=self.email)

        if email_exists:
            raise ValueError(CustomerEntity.EMAIL_IN_USE.value)

    async def check_phone(self, session: AsyncSession, repository: ICustomerRepository) -> None:
        """Ejecuta validaciones para el número de teléfono del cliente."""

        # Validar que el número de teléfono no esté registrado en la base de datos
        phone_exists = await repository.exists(session, phone=self.phone)

        if phone_exists:
            raise ValueError(CustomerEntity.PHONE_IN_USE.value)

    async def check_document_number(
        self,
        repository: ICustomerRepository,
        session: AsyncSession,
    ) -> None:
        """Ejecuta validaciones para el número de documento del cliente."""

        # Validar que el número de documento no esté registrado en la base de datos
        document_exists = await repository.exists(session, document_number=self.document_number)

        if document_exists:
            raise ValueError(CustomerEntity.DOCUMENT_NUMBER_IN_USE.value)


class ReadCustomerDTO(BaseModel):
    """DTO para la lectura de un cliente"""

    id: UUID
    first_names: str
    last_names: str
    document_type: str
    document_number: str
    phone: str
