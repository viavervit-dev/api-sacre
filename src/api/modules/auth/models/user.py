from datetime import UTC, datetime
from uuid import UUID, uuid4

import bcrypt
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.modules.auth.constants import UserEntity
from src.api.modules.auth.models.permission import Group
from src.api.modules.users.models.admin import Admin
from src.api.modules.users.models.customer import Customer
from src.api.modules.users.models.customer_wholesale import CustomerWholesale
from src.api.settings.database import ModelBase

# Constantes para validaciones de campos numéricos
SESSION_VERSION_MIN_VALUE = UserEntity.SESSION_VERSION_MIN_VALUE.value


class User(ModelBase):
    """Modelo ORM para la entidad de usuario y credenciales de autenticación."""

    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_id_role", "id", "role"),
        {"schema": "auth"},
    )

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(length=UserEntity.EMAIL_MAX_LENGTH.value),
        doc=UserEntity.EMAIL_DESCRIPTION.value,
        nullable=False,
        unique=True,
    )
    password_hash: Mapped[str] = mapped_column(
        String(length=UserEntity.PASSWORD_HASH_MAX_LENGTH.value),
        doc=UserEntity.PASSWORD_HASH_DESCRIPTION.value,
        nullable=False,
    )
    role: Mapped[str] = mapped_column(
        String(length=UserEntity.ROLE_MAX_LENGTH.value),
        doc=UserEntity.ROLE_NAME_DESCRIPTION.value,
        nullable=False,
    )
    session_version: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            sqltext=f"session_version >= {SESSION_VERSION_MIN_VALUE}",
            name="session_version_range",
        ),
        doc=UserEntity.SESSION_VERSION_DESCRIPTION.value,
        nullable=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )

    customer: Mapped[Customer] = relationship(
        argument="Customer",
        uselist=False,
        cascade="all, delete-orphan",
    )
    customer_wholesale: Mapped[CustomerWholesale] = relationship(
        argument="CustomerWholesale",
        uselist=False,
        cascade="all, delete-orphan",
    )
    admin: Mapped[Admin] = relationship(
        argument="Admin",
        uselist=False,
        cascade="all, delete-orphan",
    )
    groups: Mapped[list[Group]] = relationship(
        argument="Group",
        secondary="auth.user_groups",
    )

    def set_password(self, password: str) -> None:
        """Genera y almacena el hash seguro de la contraseña usando bcrypt."""

        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(
            password=password.encode(encoding="utf-8"),
            salt=salt,
        ).decode(encoding="utf-8")

    def verify_password(self, password: str) -> bool:
        """Comprueba si la contraseña en texto plano coincide con el hash almacenado."""

        try:
            return bcrypt.checkpw(
                password=password.encode(encoding="utf-8"),
                hashed_password=self.password_hash.encode(encoding="utf-8"),
            )
        except ValueError:
            return False

    def has_permission(self, permission_name: str) -> bool:
        """Determina si el usuario posee un permiso a través de sus grupos asociados."""

        for group in self.groups:
            for permission in group.permissions:
                if permission.name == permission_name:
                    return True

        return False


class UserGroup(ModelBase):
    """Modelo asociativo para la relación muchos a muchos entre usuarios y grupos."""

    __tablename__ = "user_groups"
    __table_args__ = {"schema": "auth"}

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
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
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=True,
    )
