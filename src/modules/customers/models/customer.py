from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from src.config.database import Base
from src.modules.customers.constants import CustomerEntity, DocumentTypesCustomer


class Customer(MappedAsDataclass, Base):
    """
    Entidad `Customer` y modelo ORM de la tabla `customers`. Actúa simultáneamente como entidad de
    dominio y como modelo **SQLAlchemy** para persistencia y migraciones con **Alembic**.
    """

    __tablename__ = "customers"
    __table_args__ = {"schema": "customer"}

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="auth.users.id"),
        doc=CustomerEntity.ID_USER_DESCRIPTION.value,
        nullable=False,
        unique=True,
    )
    first_names: Mapped[str] = mapped_column(
        String(length=CustomerEntity.FIRST_NAMES_MAX_LENGTH.value),
        doc=CustomerEntity.FIRST_NAMES_DESCRIPTION.value,
        nullable=True,
    )
    last_names: Mapped[str] = mapped_column(
        String(length=CustomerEntity.LAST_NAMES_MAX_LENGTH.value),
        doc=CustomerEntity.LAST_NAMES_DESCRIPTION.value,
        nullable=True,
    )
    document_type: Mapped[DocumentTypesCustomer] = mapped_column(
        Enum(enums=DocumentTypesCustomer, name="document_type_enum"),
        doc=CustomerEntity.DOCUMENT_TYPE_DESCRIPTION.value,
        nullable=True,
    )
    document_number: Mapped[str] = mapped_column(
        String(length=CustomerEntity.DOCUMENT_NUMBER_MAX_LENGTH.value),
        doc=CustomerEntity.DOCUMENT_NUMBER_DESCRIPTION.value,
        nullable=True,
        unique=True,
    )
    phone: Mapped[str] = mapped_column(
        String(length=CustomerEntity.PHONE_MAX_LENGTH.value),
        doc=CustomerEntity.PHONE_DESCRIPTION.value,
        nullable=True,
        unique=True,
    )
    id: Mapped[UUID] = mapped_column(
        doc=CustomerEntity.ID_DESCRIPTION.value,
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc=CustomerEntity.DATE_JOINED_DESCRIPTION.value,
        default_factory=lambda: datetime.now(tz=UTC),
    )
