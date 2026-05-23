from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from src.config.database import Base
from src.modules.auth.constants import GroupEntity, PermissionEntity


class Permission(MappedAsDataclass, Base):
    """
    Entidad `Permission` y modelo ORM de la tabla `permissions`. Actúa simultáneamente como entidad
    de dominio y como modelo **SQLAlchemy** para persistencia y migraciones con **Alembic**.
    """

    __tablename__ = "permissions"
    __table_args__ = {"schema": "auth"}

    name: Mapped[str] = mapped_column(
        String(length=PermissionEntity.NAME_MAX_LENGTH.value),
        doc=PermissionEntity.NAME_DESCRIPTION.value,
        unique=True,
        index=True,
    )
    id: Mapped[UUID] = mapped_column(
        doc=PermissionEntity.ID_DESCRIPTION.value,
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )
    permission_groups: Mapped[list["PermissionGroup"]] = relationship(
        "PermissionGroup",
        back_populates="permission",
        init=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc=PermissionEntity.DATE_JOINED_DESCRIPTION.value,
        default_factory=lambda: datetime.now(tz=UTC),
        nullable=False,
    )


class Group(MappedAsDataclass, Base):
    """
    Entidad `Group` y modelo ORM de la tabla `groups`. Actúa simultáneamente como entidad de
    dominio y como modelo **SQLAlchemy** para persistencia y migraciones con **Alembic**.
    """

    __tablename__ = "groups"
    __table_args__ = {"schema": "auth"}

    name: Mapped[str] = mapped_column(
        String(length=GroupEntity.NAME_MAX_LENGTH.value),
        doc=GroupEntity.NAME_DESCRIPTION.value,
        unique=True,
        index=True,
    )
    id: Mapped[UUID] = mapped_column(
        doc=GroupEntity.ID_DESCRIPTION.value,
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )
    permission_groups: Mapped[list["PermissionGroup"]] = relationship(
        "PermissionGroup",
        back_populates="group",
        init=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc=GroupEntity.DATE_JOINED_DESCRIPTION.value,
        default_factory=lambda: datetime.now(tz=UTC),
        nullable=False,
    )

    @property
    def permissions(self) -> list[Permission]:
        """Devuelve una lista de permisos asociados a este grupo."""

        return [pg.permission for pg in self.permission_groups]


class PermissionGroup(MappedAsDataclass, Base):
    """
    Entidad `PermissionGroup` y modelo ORM de la tabla `permission_groups`. Actúa simultáneamente
    como entidad de dominio y como modelo **SQLAlchemy** para persistencia y migraciones
    con **Alembic**.
    """

    __tablename__ = "permission_groups"
    __table_args__ = {"schema": "auth"}

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
    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )
    group: Mapped[Group] = relationship("Group", back_populates="permission_groups", init=False)
    permission: Mapped[Permission] = relationship(
        "Permission",
        back_populates="permission_groups",
        init=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default_factory=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
