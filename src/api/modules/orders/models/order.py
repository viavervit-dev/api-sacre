from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.api.modules.orders.constants import OrderEntity, OrderStatus
from src.api.settings.database import ModelBase

# Constantes para validaciones de campos numéricos
SUBTOTAL_MAX_VALUE = OrderEntity.SUBTOTAL_MAX_VALUE.value
SUBTOTAL_MIN_VALUE = OrderEntity.SUBTOTAL_MIN_VALUE.value
TAX_AMOUNT_MAX_VALUE = OrderEntity.TAX_AMOUNT_MAX_VALUE.value
TAX_AMOUNT_MIN_VALUE = OrderEntity.TAX_AMOUNT_MIN_VALUE.value
SHIPING_COST_MAX_VALUE = OrderEntity.SHIPING_COST_MAX_VALUE.value
SHIPING_COST_MIN_VALUE = OrderEntity.SHIPING_COST_MIN_VALUE.value
DISCOUNT_AMOUNT_MAX_VALUE = OrderEntity.DISCOUNT_AMOUNT_MAX_VALUE.value
DISCOUNT_AMOUNT_MIN_VALUE = OrderEntity.DISCOUNT_AMOUNT_MIN_VALUE.value
DISCOUNT_PERCENTAGE_MAX_VALUE = OrderEntity.DISCOUNT_PERCENTAGE_MAX_VALUE.value
DISCOUNT_PERCENTAGE_MIN_VALUE = OrderEntity.DISCOUNT_PERCENTAGE_MIN_VALUE.value
TOTAL_AMOUNT_MAX_VALUE = OrderEntity.TOTAL_AMOUNT_MAX_VALUE.value
TOTAL_AMOUNT_MIN_VALUE = OrderEntity.TOTAL_AMOUNT_MIN_VALUE.value


class Order(ModelBase):
    """Modelo ORM para la gestión de pedidos y transacciones de compra."""

    __tablename__ = "orders"
    __table_args__ = {"schema": "orders"}

    id: Mapped[UUID] = mapped_column(
        doc="Identificador interno del pedido (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    order_number: Mapped[str] = mapped_column(
        String(length=14),
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
    product_data: Mapped[dict[str, Any]] = mapped_column(
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
    currency: Mapped[str] = mapped_column(
        String(length=5),
        doc=OrderEntity.CURRENCY_DESCRIPTION.value,
        nullable=False,
    )
    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=OrderEntity.SUBTOTAL_MAX_DIGITS.value,
            scale=OrderEntity.SUBTOTAL_DECIMAL_PLACES.value,
            asdecimal=True,
        ),
        CheckConstraint(
            sqltext=f"subtotal > {SUBTOTAL_MIN_VALUE} AND subtotal <= {SUBTOTAL_MAX_VALUE}",
            name="subtotal_range",
        ),
        doc=OrderEntity.SUBTOTAL_DESCRIPTION.value,
        nullable=False,
    )
    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=OrderEntity.TAX_AMOUNT_MAX_DIGITS.value,
            scale=OrderEntity.TAX_AMOUNT_DECIMAL_PLACES.value,
            asdecimal=True,
        ),
        CheckConstraint(
            sqltext=f"tax_amount >= {TAX_AMOUNT_MIN_VALUE} AND tax_amount <= {TAX_AMOUNT_MAX_VALUE}",  # noqa: E501
            name="tax_amount_range",
        ),
        doc=OrderEntity.TAX_AMOUNT_DESCRIPTION.value,
        nullable=False,
    )
    shipping_cost: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=OrderEntity.SHIPING_COST_MAX_DIGITS.value,
            scale=OrderEntity.SHIPING_COST_DECIMAL_PLACES.value,
            asdecimal=True,
        ),
        CheckConstraint(
            sqltext=f"shipping_cost >= {SHIPING_COST_MIN_VALUE} AND shipping_cost <= {SHIPING_COST_MAX_VALUE}",  # noqa: E501
            name="shipping_cost_range",
        ),
        doc=OrderEntity.SHIPING_COST_DESCRIPTION.value,
        nullable=False,
    )
    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=OrderEntity.DISCOUNT_AMOUNT_MAX_DIGITS.value,
            scale=OrderEntity.DISCOUNT_AMOUNT_DECIMAL_PLACES.value,
            asdecimal=True,
        ),
        CheckConstraint(
            sqltext=f"discount_amount >= {DISCOUNT_AMOUNT_MIN_VALUE} AND discount_amount <= {DISCOUNT_AMOUNT_MAX_VALUE}",  # noqa: E501
            name="discount_amount_range",
        ),
        doc=OrderEntity.DISCOUNT_AMOUNT_DESCRIPTION.value,
        nullable=False,
    )
    discount_percentage: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=OrderEntity.DISCOUNT_PERCENTAGE_MAX_DIGITS.value,
            scale=OrderEntity.DISCOUNT_PERCENTAGE_DECIMAL_PLACES.value,
            asdecimal=True,
        ),
        CheckConstraint(
            sqltext=f"discount_percentage >= {DISCOUNT_PERCENTAGE_MIN_VALUE} AND discount_percentage <= {DISCOUNT_PERCENTAGE_MAX_VALUE}",  # noqa: E501
            name="discount_percentage_range",
        ),
        doc=OrderEntity.DISCOUNT_PERCENTAGE_DESCRIPTION.value,
        nullable=False,
    )
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=OrderEntity.TOTAL_AMOUNT_MAX_DIGITS.value,
            scale=OrderEntity.TOTAL_AMOUNT_DECIMAL_PLACES.value,
            asdecimal=True,
        ),
        CheckConstraint(
            sqltext=f"total_amount >= {TOTAL_AMOUNT_MIN_VALUE} AND total_amount <= {TOTAL_AMOUNT_MAX_VALUE}",  # noqa: E501
            name="total_amount_range",
        ),
        doc=OrderEntity.TOTAL_AMOUNT_DESCRIPTION.value,
        nullable=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
