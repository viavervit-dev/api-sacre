from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLAlchemyUUID
from sqlalchemy import CheckConstraint, DateTime, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.api.modules.orders.constants import OrderEntity, OrderStatus
from src.api.settings.database import ModelBase

# Constantes para validaciones de campos numéricos
SUBTOTAL_MAX_VALUE = OrderEntity.SUBTOTAL_MAX_VALUE.value
SUBTOTAL_MIN_VALUE = OrderEntity.SUBTOTAL_MIN_VALUE.value
TAX_AMOUNT_MAX_VALUE = OrderEntity.TAX_AMOUNT_MAX_VALUE.value
TAX_AMOUNT_MIN_VALUE = OrderEntity.TAX_AMOUNT_MIN_VALUE.value
TOTAL_MAX_VALUE = OrderEntity.TOTAL_MAX_VALUE.value
TOTAL_MIN_VALUE = OrderEntity.TOTAL_MIN_VALUE.value
UNITS_MAX_VALUE = OrderEntity.UNITS_MAX_VALUE.value
UNITS_MIN_VALUE = OrderEntity.UNITS_MIN_VALUE.value


class Order(ModelBase):
    """Modelo ORM para la gestión de pedidos y transacciones de compra."""

    __tablename__ = "orders"
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
    order_number: Mapped[UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        doc=OrderEntity.ORDER_NUMBER_DESCRIPTION.value,
        unique=True,
        nullable=False,
        index=True,
    )
    customer_data: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        doc=OrderEntity.CUSTOMER_DATA_DESCRIPTION.value,
        nullable=False,
    )
    product_data: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB,
        doc=OrderEntity.PRODUCT_DATA_DESCRIPTION.value,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(length=100),
        doc=OrderEntity.STATUS_DESCRIPTION.value,
        default=OrderStatus.PENDING_PAYMENT,
        nullable=False,
        index=True,
    )
    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=OrderEntity.SUBTOTAL_MAX_DIGITS.value,
            scale=OrderEntity.SUBTOTAL_DECIMAL_PLACES.value,
            asdecimal=True,
        ),
        doc=OrderEntity.SUBTOTAL_DESCRIPTION.value,
        nullable=False,
    )
    total: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=OrderEntity.TOTAL_MAX_DIGITS.value,
            scale=OrderEntity.TOTAL_DECIMAL_PLACES.value,
            asdecimal=True,
        ),
        doc=OrderEntity.TOTAL_DESCRIPTION.value,
        nullable=False,
    )
    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=OrderEntity.TAX_AMOUNT_MAX_DIGITS.value,
            scale=OrderEntity.TAX_AMOUNT_DECIMAL_PLACES.value,
            asdecimal=True,
        ),
        doc=OrderEntity.TAX_AMOUNT_DESCRIPTION.value,
        nullable=False,
    )
    units: Mapped[int] = mapped_column(
        Integer,
        doc=OrderEntity.UNITS_DESCRIPTION.value,
        nullable=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
