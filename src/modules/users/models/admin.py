from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base
from src.modules.users.constants import AdminEntity


class Admin(Base):
    """
    Modelo ORM para el perfil de usuario administrador.

    Almacena los datos personales del administrador en el esquema `admin` y se
    vincula directamente mediante una relación uno a uno con la cuenta base `User`.
    """

    __tablename__ = "admins"
    __table_args__ = {"schema": "users"}

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="auth.users.id"),
        doc=AdminEntity.ID_USER_DESCRIPTION.value,
        unique=True,
        nullable=False,
    )
    first_names: Mapped[str] = mapped_column(
        String(length=AdminEntity.FIRST_NAMES_MAX_LENGTH.value),
        doc=AdminEntity.FIRST_NAMES_DESCRIPTION.value,
        nullable=False,
    )
    last_names: Mapped[str] = mapped_column(
        String(length=AdminEntity.LAST_NAMES_MAX_LENGTH.value),
        doc=AdminEntity.LAST_NAMES_DESCRIPTION.value,
        nullable=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
