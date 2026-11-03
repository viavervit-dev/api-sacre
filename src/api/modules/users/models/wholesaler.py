from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import ARRAY, DateTime, ForeignKey, String
from sqlalchemy import UUID as SQLAlchemyUUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.api.modules.users.constants import WholesalerEntity
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
        doc=WholesalerEntity.PRODUCTS_DESCRIPTION.value,
        nullable=False,
    )
    name_or_company_name: Mapped[str] = mapped_column(
        String(length=WholesalerEntity.NAME_OR_COMPANY_NAME_MAX_LENGTH.value),
        doc=WholesalerEntity.NAME_OR_COMPANY_NAME_DESCRIPTION.value,
        nullable=False,
        unique=True,
    )
    ruc: Mapped[str | None] = mapped_column(
        String(length=WholesalerEntity.RUC_MAX_LENGTH.value),
        doc=WholesalerEntity.RUC_DESCRIPTION.value,
        nullable=True,
        unique=True,
    )
    phone: Mapped[str] = mapped_column(
        String(length=WholesalerEntity.PHONE_MAX_LENGTH.value),
        doc=WholesalerEntity.PHONE_DESCRIPTION.value,
        nullable=False,
        unique=True,
    )
    location: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        doc=WholesalerEntity.LOCATION_DESCRIPTION.value,
        nullable=False,
    )
    extra_contacts: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        doc=WholesalerEntity.EXTRA_CONTACTS_DESCRIPTION.value,
        nullable=True,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
