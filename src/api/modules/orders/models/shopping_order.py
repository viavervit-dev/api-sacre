from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLAlchemyUUID
from sqlalchemy import CheckConstraint, DateTime, Integer, Numeric, Sequence, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.api.modules.orders.constants import ShoppingOrderEntity
from src.api.settings.database import ModelBase

# Constantes para validaciones de campos numéricos
SUBTOTAL_MAX_VALUE = ShoppingOrderEntity.SUBTOTAL_MAX_VALUE.value
SUBTOTAL_MIN_VALUE = ShoppingOrderEntity.SUBTOTAL_MIN_VALUE.value
TAX_AMOUNT_MAX_VALUE = ShoppingOrderEntity.TAX_AMOUNT_MAX_VALUE.value
TAX_AMOUNT_MIN_VALUE = ShoppingOrderEntity.TAX_AMOUNT_MIN_VALUE.value
TOTAL_MAX_VALUE = ShoppingOrderEntity.TOTAL_MAX_VALUE.value
TOTAL_MIN_VALUE = ShoppingOrderEntity.TOTAL_MIN_VALUE.value
UNITS_MAX_VALUE = ShoppingOrderEntity.UNITS_MAX_VALUE.value
UNITS_MIN_VALUE = ShoppingOrderEntity.UNITS_MIN_VALUE.value


# Secuencia atómica para el número de ordenes de compra
shopping_order_number_seq = Sequence(
    name="shopping_order_number_seq",
    schema="orders",
    start=1,
    metadata=ModelBase.metadata,
)


class ShoppingOrder(ModelBase):
    """Modelo ORM para la gestión de ordenes de compra."""

    __tablename__ = "shopping_orders"
    __table_args__ = (
        CheckConstraint(
            sqltext=f"subtotal > {SUBTOTAL_MIN_VALUE} AND subtotal <= {SUBTOTAL_MAX_VALUE}",
            name="subtotal_range",
        ),
        CheckConstraint(
            sqltext=f"total > {TOTAL_MIN_VALUE} AND total <= {TOTAL_MAX_VALUE}",
            name="totals_range",
        ),
        CheckConstraint(
            sqltext=f"tax_amount > {TAX_AMOUNT_MIN_VALUE} AND tax_amount <= {TAX_AMOUNT_MAX_VALUE}",  # noqa: E501
            name="tax_amount_range",
        ),
        CheckConstraint(
            sqltext=f"units > {UNITS_MIN_VALUE} AND units <= {UNITS_MAX_VALUE}",
            name="units_range",
        ),
        {"schema": "orders"},
    )

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    idempotency_key: Mapped[UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        doc=ShoppingOrderEntity.IDEMPOTENCY_KEY_DESCRIPTION.value,
        unique=True,
        nullable=False,
        index=True,
    )
    order_number: Mapped[str] = mapped_column(
        String(length=15),
        doc=ShoppingOrderEntity.ORDER_NUMBER_DESCRIPTION.value,
        unique=True,
        nullable=False,
    )
    customer_data: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        doc=ShoppingOrderEntity.CUSTOMER_DATA_DESCRIPTION.value,
        nullable=False,
    )
    product_data: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB,
        doc=ShoppingOrderEntity.PRODUCT_DATA_DESCRIPTION.value,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(length=200),
        doc=ShoppingOrderEntity.ORDER_DESCRIPTION.value,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(length=100),
        doc=ShoppingOrderEntity.STATUS_DESCRIPTION.value,
        nullable=False,
        index=True,
    )
    status_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la última modificación de estado.",
        nullable=True,
    )
    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=ShoppingOrderEntity.SUBTOTAL_MAX_DIGITS.value,
            scale=ShoppingOrderEntity.SUBTOTAL_DECIMAL_PLACES.value,
            asdecimal=True,
        ),
        doc=ShoppingOrderEntity.SUBTOTAL_DESCRIPTION.value,
        nullable=False,
    )
    total: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=ShoppingOrderEntity.TOTAL_MAX_DIGITS.value,
            scale=ShoppingOrderEntity.TOTAL_DECIMAL_PLACES.value,
            asdecimal=True,
        ),
        doc=ShoppingOrderEntity.TOTAL_DESCRIPTION.value,
        nullable=False,
    )
    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=ShoppingOrderEntity.TAX_AMOUNT_MAX_DIGITS.value,
            scale=ShoppingOrderEntity.TAX_AMOUNT_DECIMAL_PLACES.value,
            asdecimal=True,
        ),
        doc=ShoppingOrderEntity.TAX_AMOUNT_DESCRIPTION.value,
        nullable=False,
    )
    units: Mapped[int] = mapped_column(
        Integer,
        doc=ShoppingOrderEntity.UNITS_DESCRIPTION.value,
        nullable=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
