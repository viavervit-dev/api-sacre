from datetime import UTC, datetime
from uuid import UUID, uuid4

from passlib.context import CryptContext
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from src.config.database import Base
from src.modules.authentication.constants import UserEntity
from src.modules.authentication.models.permission import Group

# Configuración de PassLib para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserGroup(MappedAsDataclass, Base):
    """
    Entidad `UserGroup` y modelo ORM de la tabla `user_groups`. Actúa simultáneamente como entidad
    de dominio y como modelo **SQLAlchemy** para persistencia y migraciones con **Alembic**.
    """

    __tablename__ = "auth.user_groups"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        doc="ID del usuario referenciado",
        nullable=False,
    )
    group_id: Mapped[UUID] = mapped_column(
        ForeignKey("auth.groups.id", ondelete="CASCADE"),
        doc="ID del grupo referenciado",
        nullable=False,
    )
    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )
    user: Mapped["User"] = relationship("User", backref="user_groups", default=None)
    group: Mapped[Group] = relationship("Group", backref="user_groups", default=None)
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default_factory=lambda: datetime.now(tz=UTC),
    )


class User(MappedAsDataclass, Base):
    """
    Entidad `User` y modelo ORM de la tabla `users`. Actúa simultáneamente como entidad de dominio
    y como modelo **SQLAlchemy** para persistencia y migraciones con **Alembic**.
    """

    __tablename__ = "auth.users"

    email: Mapped[str] = mapped_column(
        String(length=UserEntity.EMAIL_MAX_LENGTH.value),
        doc=UserEntity.EMAIL_DESCRIPTION.value,
        unique=True,
    )
    password_hash: Mapped[str] = mapped_column(
        String(length=UserEntity.PASSWORD_HASH_MAX_LENGTH.value),
        doc=UserEntity.PASSWORD_HASH_DESCRIPTION.value,
        nullable=False,
    )
    permission_groups_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="auth.groups.id", ondelete="CASCADE"),
        doc="ID de la permission referenciada",
        nullable=False,
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
        backref="users",
        default=None,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc=UserEntity.DATE_JOINED_DESCRIPTION.value,
        default_factory=lambda: datetime.now(tz=UTC),
    )

    def set_password(self, password: str) -> None:
        """Guarda el hash encriptado de la contraseña."""

        self.password_hash = pwd_context.hash(secret=password)

    def verify_password(self, password: str) -> bool:
        """Verifica si la contraseña proporcionada coincide con el hash almacenado."""

        return pwd_context.verify(secret=password, hash=self.password_hash)
