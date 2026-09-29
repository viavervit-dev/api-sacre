from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base
from src.modules.users.constants import WholesaleEntity


class Wholesale(Base):
    """
    Modelo ORM para el perfil de cliente mayorista.

    Gestiona la información comercial, identificación tributaria (RUC), canales de
    contacto y ubicación geográfica en el esquema `users` (`users.wholesale`).
    """

    __tablename__ = "wholesale"
    __table_args__ = {"schema": "users"}

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    name_or_company_name: Mapped[str] = mapped_column(
        String(length=WholesaleEntity.NAME_OR_COMPANY_NAME_MAX_LENGTH.value),
        doc=WholesaleEntity.NAME_OR_COMPANY_NAME_DESCRIPTION.value,
        nullable=False,
        unique=True,
    )
    email: Mapped[str] = mapped_column(
        String(length=WholesaleEntity.EMAIL_MAX_LENGTH.value),
        doc=WholesaleEntity.EMAIL_DESCRIPTION.value,
        nullable=False,
        unique=True,
    )
    ruc: Mapped[str | None] = mapped_column(
        String(length=WholesaleEntity.RUC_MAX_LENGTH.value),
        doc=WholesaleEntity.RUC_DESCRIPTION.value,
        nullable=True,
        unique=True,
    )
    phone: Mapped[str] = mapped_column(
        String(length=WholesaleEntity.PHONE_MAX_LENGTH.value),
        doc=WholesaleEntity.PHONE_DESCRIPTION.value,
        nullable=False,
        unique=True,
    )
    location: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        doc=WholesaleEntity.LOCATION_DESCRIPTION.value,
        nullable=False,
    )
    extra_contacts: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        doc=WholesaleEntity.EXTRA_CONTACTS_DESCRIPTION.value,
        nullable=True,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
