from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.api.modules.payments.constants import PaymentEntity
from src.api.settings.database import ModelBase


class Payment(ModelBase):
    """Modelo ORM para la gestión de pagos."""

    __tablename__ = "payments"
    __table_args__ = {"schema": "payments"}

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    shopping_order_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="orders.shopping_orders.id"),
        doc="Identificador único de la cuenta de la orden de compra.",
        nullable=False,
        unique=True,
    )
    type: Mapped[str] = mapped_column(
        String(length=20),
        doc=PaymentEntity.TYPE_DESCRIPTION.value,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(length=100),
        doc=PaymentEntity.STATUS_DESCRIPTION.value,
        nullable=False,
        index=True,
    )
    status_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la última modificación de estado.",
        nullable=True,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
