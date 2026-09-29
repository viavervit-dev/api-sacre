from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class Country(Base):
    """
    Modelo ORM para la gestión de países y divisiones territoriales.

    Centraliza el catálogo geográfico en el esquema `countries` (`countries.country`),
    almacenando el nombre oficial de cada país y la definición jerárquica de su
    estructura político-administrativa.
    """

    __tablename__ = "country"
    __table_args__ = {"schema": "countries"}

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(length=60),
        doc="Nombre del país.",
        nullable=False,
        unique=True,
    )
    administrative_structure: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        doc="Estructura y organización territorial del país.",
        nullable=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
