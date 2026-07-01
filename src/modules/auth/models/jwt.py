from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from src.config.database import Base
from src.modules.auth.constants import JWTEntity


class JWTBlacklist(MappedAsDataclass, Base):
    """
    Entidad `JWTBlacklist` y modelo ORM de la tabla `jwt_blacklist`. Actúa simultáneamente como
    entidad de dominio y como modelo **SQLAlchemy** para persistencia y migraciones con
    **Alembic**.
    """

    __tablename__ = "json_web_token_blacklist"
    __table_args__ = {"schema": "auth"}

    token: Mapped[str] = mapped_column(
        String(length=JWTEntity.TOKEN_MAX_LENGTH.value),
        doc=JWTEntity.TOKEN_DESCRIPTION.value,
        unique=True,
        nullable=True,
    )
    jti: Mapped[str] = mapped_column(
        String(length=JWTEntity.JTI_MAX_LENGTH.value),
        doc=JWTEntity.JTI_DESCRIPTION.value,
        unique=True,
        index=True,
        nullable=True,
    )
    token_type: Mapped[str] = mapped_column(
        String(length=JWTEntity.TOKEN_TYPE_MAX_LENGTH.value),
        doc=JWTEntity.TOKEN_TYPE_DESCRIPTION.value,
        unique=True,
        index=True,
        nullable=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="auth.users.id", ondelete="CASCADE"),
        doc=JWTEntity.USER_ID_DESCRIPTION.value,
        nullable=True,
    )
    id: Mapped[UUID] = mapped_column(
        doc=JWTEntity.ID_DESCRIPTION.value,
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc=JWTEntity.DATE_JOINED_DESCRIPTION.value,
        default_factory=lambda: datetime.now(tz=UTC),
        nullable=True,
    )
