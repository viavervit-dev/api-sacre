from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.api.modules.users.constants import CustomerEntity
from src.api.settings.database import ModelBase


class Customer(ModelBase):
    """Modelo ORM para el perfil de un cliente."""

    __tablename__ = "customers"
    __table_args__ = {"schema": "users"}

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="auth.users.id"),
        doc="Identificador único de la cuenta de usuario vinculada a este perfil.",
        nullable=False,
        unique=True,
    )
    first_names: Mapped[str] = mapped_column(
        String(length=CustomerEntity.FIRST_NAMES_MAX_LENGTH.value),
        doc=CustomerEntity.FIRST_NAMES_DESCRIPTION.value,
        nullable=False,
    )
    last_names: Mapped[str] = mapped_column(
        String(length=CustomerEntity.LAST_NAMES_MAX_LENGTH.value),
        doc=CustomerEntity.LAST_NAMES_DESCRIPTION.value,
        nullable=False,
    )
    document_type: Mapped[str | None] = mapped_column(
        String(length=CustomerEntity.DOCUMENT_TYPE_MAX_LENGTH.value),
        doc=CustomerEntity.DOCUMENT_TYPE_DESCRIPTION.value,
        nullable=True,
    )
    document_number: Mapped[str | None] = mapped_column(
        String(length=CustomerEntity.DOCUMENT_NUMBER_MAX_LENGTH.value),
        doc=CustomerEntity.DOCUMENT_NUMBER_DESCRIPTION.value,
        nullable=True,
        unique=True,
    )
    phone: Mapped[str | None] = mapped_column(
        String(length=CustomerEntity.PHONE_MAX_LENGTH.value),
        doc=CustomerEntity.PHONE_DESCRIPTION.value,
        nullable=True,
        unique=True,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
