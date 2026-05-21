from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from src.config.database import Base
from src.modules.admins.constants import AdminEntity


class Admin(MappedAsDataclass, Base):
    """
    Entidad `Admin` y modelo ORM de la tabla `admins`. Actúa simultáneamente como entidad de
    dominio y como modelo **SQLAlchemy** para persistencia y migraciones con **Alembic**.
    """

    __tablename__ = "admins"
    __table_args__ = {"schema": "admin"}

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="auth.users.id"),
        doc=AdminEntity.ID_USER_DESCRIPTION.value,
        nullable=False,
        unique=True,
    )
    first_names: Mapped[str] = mapped_column(
        String(length=AdminEntity.FIRST_NAMES_MAX_LENGTH.value),
        doc=AdminEntity.FIRST_NAMES_DESCRIPTION.value,
        nullable=True,
    )
    last_names: Mapped[str] = mapped_column(
        String(length=AdminEntity.LAST_NAMES_MAX_LENGTH.value),
        doc=AdminEntity.LAST_NAMES_DESCRIPTION.value,
        nullable=True,
    )
    id: Mapped[UUID] = mapped_column(
        doc=AdminEntity.ID_DESCRIPTION.value,
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc=AdminEntity.DATE_JOINED_DESCRIPTION.value,
        default_factory=lambda: datetime.now(tz=UTC),
    )
