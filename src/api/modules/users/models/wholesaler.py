from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import ARRAY, DateTime, ForeignKey, String
from sqlalchemy import UUID as SQLAlchemyUUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.api.modules.users.constants.wholesaler import WHOLESALER_CONSTANTS
from src.api.settings.database import ModelBase


class Wholesaler(ModelBase):
    """Modelo ORM para el perfil de un cliente mayorista."""

    __tablename__ = "wholesaler"
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
    products: Mapped[list[UUID]] = mapped_column(
        ARRAY(item_type=SQLAlchemyUUID(as_uuid=True)),
        doc=WHOLESALER_CONSTANTS.Docs.PRODUCTS_DESCRIPTION,
        nullable=False,
    )
    name_or_company_name: Mapped[str] = mapped_column(
        String(length=WHOLESALER_CONSTANTS.Limits.NAME_OR_COMPANY_NAME_MAX_LENGTH),
        doc=WHOLESALER_CONSTANTS.Docs.NAME_OR_COMPANY_NAME_DESCRIPTION,
        nullable=False,
        unique=True,
    )
    ruc: Mapped[str | None] = mapped_column(
        String(length=WHOLESALER_CONSTANTS.Limits.RUC_MAX_LENGTH),
        doc=WHOLESALER_CONSTANTS.Docs.RUC_DESCRIPTION,
        nullable=True,
        unique=True,
    )
    phone: Mapped[str] = mapped_column(
        String(length=WHOLESALER_CONSTANTS.Limits.PHONE_MAX_LENGTH),
        doc=WHOLESALER_CONSTANTS.Docs.PHONE_DESCRIPTION,
        nullable=False,
        unique=True,
    )
    location: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        doc=WHOLESALER_CONSTANTS.Docs.LOCATION_DESCRIPTION,
        nullable=False,
    )
    extra_contacts: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        doc=WHOLESALER_CONSTANTS.Docs.EXTRA_CONTACTS_DESCRIPTION,
        nullable=True,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
