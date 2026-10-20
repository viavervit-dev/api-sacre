from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.modules.auth.constants import GroupEntity, PermissionEntity
from src.api.settings.database import ModelBase


class Permission(ModelBase):
    """Modelo ORM que define un permiso de acceso o acción en el sistema."""

    __tablename__ = "permissions"
    __table_args__ = {"schema": "auth"}

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(length=PermissionEntity.NAME_MAX_LENGTH.value),
        doc=PermissionEntity.NAME_DESCRIPTION.value,
        nullable=False,
        unique=True,
        index=True,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )

    groups: Mapped[list[Group]] = relationship(
        argument="Group",
        back_populates="permissions",
        secondary="auth.permission_groups",
    )


class Group(ModelBase):
    """Modelo ORM para la agrupación y gestión colectiva de permisos."""

    __tablename__ = "groups"
    __table_args__ = {"schema": "auth"}

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(length=GroupEntity.NAME_MAX_LENGTH.value),
        doc=GroupEntity.NAME_DESCRIPTION.value,
        nullable=False,
        unique=True,
        index=True,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )

    permissions: Mapped[list[Permission]] = relationship(
        argument="Permission",
        secondary="auth.permission_groups",
        back_populates="groups",
    )


class PermissionGroup(ModelBase):
    """Modelo asociativo para la relación muchos a muchos entre permisos y grupos."""

    __tablename__ = "permission_groups"
    __table_args__ = {"schema": "auth"}

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    permission_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="auth.permissions.id", ondelete="CASCADE"),
        doc="ID del permiso referenciado",
        nullable=False,
    )
    group_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="auth.groups.id", ondelete="CASCADE"),
        doc="ID del grupo referenciado",
        nullable=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
