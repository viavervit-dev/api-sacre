from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class ProvinceEcuador(Base):
    """
    Modelo ORM para las provincias del Ecuador.

    Representa el primer nivel de división político-administrativa del país en el
    esquema `countries` (`countries.province_ecuador`), registrando el nombre oficial
    de cada provincia.
    """

    __tablename__ = "province_ecuador"
    __table_args__ = {"schema": "countries"}

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(length=100),
        doc="Nombre oficial de la provincia.",
        nullable=False,
        unique=True,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )


class CantonEcuador(Base):
    """
    Modelo ORM para los cantones del Ecuador.

    Representa el segundo nivel de división político-administrativa del país en el
    esquema `countries` (`countries.canton_ecuador`), registrando cada uno de los
    cantones o municipalidades que conforman las provincias.
    """

    __tablename__ = "canton_ecuador"
    __table_args__ = {"schema": "countries"}

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(length=100),
        doc="Nombre oficial del cantón.",
        nullable=False,
        unique=True,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )


class CityEcuador(Base):
    """
    Modelo ORM para las ciudades del Ecuador.

    Representa los centros urbanos y localidades principales del país en el esquema
    `countries` (`countries.city_ecuador`), almacenando su denominación oficial.
    """

    __tablename__ = "city_ecuador"
    __table_args__ = {"schema": "countries"}

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(length=100),
        doc="Nombre oficial de la ciudad o localidad.",
        nullable=False,
        unique=True,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )


class OrganizationEcuador(Base):
    """
    Modelo ORM para la estructura territorial jerárquica del Ecuador.

    Centraliza la relación jerárquica entre provincias, cantones y ciudades en el
    esquema `countries` (`countries.organization_ecuador`), facilitando la
    ubicación geográfica precisa en el sistema.
    """

    __tablename__ = "organization_ecuador"
    __table_args__ = {"schema": "countries"}

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    country_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="countries.country.id", ondelete="CASCADE"),
        doc="ID de la provincia referenciada.",
        nullable=False,
    )
    province_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="countries.province_ecuador.id", ondelete="CASCADE"),
        doc="ID de la provincia referenciada.",
        nullable=False,
    )
    canton_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="countries.canton_ecuador.id", ondelete="CASCADE"),
        doc="ID del cantón referenciado.",
        nullable=False,
    )
    city_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="countries.city_ecuador.id", ondelete="CASCADE"),
        doc="ID de la ciudad referenciada.",
        nullable=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
