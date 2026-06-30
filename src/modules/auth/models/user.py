from datetime import UTC, datetime
from uuid import UUID, uuid4

import bcrypt
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, MappedAsDataclass, backref, mapped_column, relationship

from src.config.database import Base
from src.modules.admins.models.admin import Admin
from src.modules.auth.constants import UserEntity
from src.modules.auth.models.permission import Group
from src.modules.customers.models.customer import Customer

# Constantes para validaciones de campos numéricos
SESSION_VERSION_MIN_VALUE = UserEntity.SESSION_VERSION_MIN_VALUE.value


class User(MappedAsDataclass, Base):
    """
    Entidad `User` y modelo ORM de la tabla `users`. Actúa simultáneamente como entidad de dominio
    y como modelo **SQLAlchemy** para persistencia y migraciones con **Alembic**.
    """

    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}

    customer: Mapped[Customer] = relationship(
        "Customer",
        uselist=False,
        back_populates=None,
        cascade="all, delete-orphan",
        init=False,
    )
    admin: Mapped[Admin] = relationship(
        "Admin",
        uselist=False,
        back_populates=None,
        cascade="all, delete-orphan",
        init=False,
    )
    email: Mapped[str] = mapped_column(
        String(length=UserEntity.EMAIL_MAX_LENGTH.value),
        doc=UserEntity.EMAIL_DESCRIPTION.value,
        unique=True,
        nullable=True,
    )
    password_hash: Mapped[str] = mapped_column(
        String(length=UserEntity.PASSWORD_HASH_MAX_LENGTH.value),
        doc=UserEntity.PASSWORD_HASH_DESCRIPTION.value,
        nullable=True,
        init=False,
    )
    role: Mapped[str] = mapped_column(
        String(length=UserEntity.ROLE_MAX_LENGTH.value),
        doc=UserEntity.ROLE_NAME_DESCRIPTION.value,
        nullable=True,
    )
    session_version: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            sqltext=f"session_version >= {SESSION_VERSION_MIN_VALUE}",
            name="session_version_range",
        ),
        doc=UserEntity.SESSION_VERSION_DESCRIPTION.value,
        nullable=True,
    )
    id: Mapped[UUID] = mapped_column(
        doc=UserEntity.ID_DESCRIPTION.value,
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )
    groups: Mapped[list[Group]] = relationship(
        "Group",
        secondary="auth.user_groups",
        backref=backref("users", overlaps="groups,user_groups"),
        init=False,
        overlaps="user_groups",
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc=UserEntity.DATE_JOINED_DESCRIPTION.value,
        default_factory=lambda: datetime.now(tz=UTC),
        nullable=True,
    )

    def set_password(self, password: str) -> None:
        """Guarda el hash encriptado de la contraseña."""

        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(
            password=password.encode(encoding="utf-8"),
            salt=salt,
        ).decode(encoding="utf-8")

    def verify_password(self, password: str) -> bool:
        """Verifica si la contraseña proporcionada coincide con el hash almacenado."""

        try:
            return bcrypt.checkpw(
                password=password.encode(encoding="utf-8"),
                hashed_password=self.password_hash.encode(encoding="utf-8"),
            )
        except ValueError:
            return False

    def has_permission(self, permission_name: str) -> bool:
        """Verifica si el usuario tiene un permiso específico."""

        for group in self.groups:
            for permission in group.permissions:
                if permission.name == permission_name:
                    return True

        return False


class UserGroup(MappedAsDataclass, Base):
    """
    Entidad `UserGroup` y modelo ORM de la tabla `user_groups`. Actúa simultáneamente como entidad
    de dominio y como modelo **SQLAlchemy** para persistencia y migraciones con **Alembic**.
    """

    __tablename__ = "user_groups"
    __table_args__ = {"schema": "auth"}

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="auth.users.id", ondelete="CASCADE"),
        doc="ID del usuario referenciado",
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
    user: Mapped[User] = relationship(
        "User",
        backref=backref("user_groups", overlaps="groups,users"),
        init=False,
        overlaps="groups,users",
    )
    group: Mapped[Group] = relationship(
        "Group",
        backref=backref("user_groups", overlaps="groups,users"),
        init=False,
        overlaps="groups,users",
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default_factory=lambda: datetime.now(tz=UTC),
        nullable=True,
    )
