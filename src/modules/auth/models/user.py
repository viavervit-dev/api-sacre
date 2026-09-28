from datetime import UTC, datetime
from uuid import UUID, uuid4

import bcrypt
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base
from src.modules.auth.constants import UserEntity
from src.modules.auth.models.permission import Group
from src.modules.users.models.admin import Admin
from src.modules.users.models.customer import Customer

# Constantes para validaciones de campos numéricos
SESSION_VERSION_MIN_VALUE = UserEntity.SESSION_VERSION_MIN_VALUE.value


class User(Base):
    """
    Modelo ORM para la entidad de usuario y credenciales de autenticación.

    Gestiona el acceso al sistema, ciclo de vida de sesiones, roles y la
    vinculación con perfiles específicos y grupos de permisos.
    """

    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}

    id: Mapped[UUID] = mapped_column(
        doc=UserEntity.ID_DESCRIPTION.value,
        default=uuid4,
        primary_key=True,
        nullable=False,
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
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc=UserEntity.DATE_JOINED_DESCRIPTION.value,
        default=lambda: datetime.now(tz=UTC),
        nullable=True,
    )

    customer: Mapped[Customer] = relationship(
        argument="Customer",
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


class UserGroup(Base):
    """
    Modelo asociativo para la relación muchos a muchos entre usuarios y grupos.

    Representa la tabla intermedia `auth.user_groups` que vincula las entidades
    `User` y `Group`.
    """

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
