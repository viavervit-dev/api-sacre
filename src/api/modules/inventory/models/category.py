from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.api.modules.inventory.constants import CategoryEntity
from src.api.settings.database import ModelBase


class Category(ModelBase):
    """Modelo ORM para la clasificación y categorización de productos en el inventario."""

    __tablename__ = "categories"
    __table_args__ = {"schema": "inventory"}

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(length=CategoryEntity.NAME_MAX_LENGTH.value),
        doc=CategoryEntity.NAME_DESCRIPTION.value,
        nullable=False,
        unique=True,
    )
    description: Mapped[str] = mapped_column(
        String(length=CategoryEntity.DESCRIPTION_MAX_LENGTH.value),
        doc=CategoryEntity.DESCRIPTION_DESCRIPTION.value,
        nullable=False,
    )
    status: Mapped[bool] = mapped_column(
        Boolean,
        doc=CategoryEntity.STATUS_DESCRIPTION.value,
        nullable=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
