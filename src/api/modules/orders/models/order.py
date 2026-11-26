# ruff: noqa: E501

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLAlchemyUUID
from sqlalchemy import CheckConstraint, DateTime, Index, Integer, Numeric, Sequence, String, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.api.modules.orders.constants.purchase import ORDER_CONSTANTS
from src.api.settings.database import ModelBase

# Constantes para validaciones de campos numéricos
SUBTOTAL_MAX_VALUE = ORDER_CONSTANTS.Limits.SUBTOTAL_MAX_VALUE
SUBTOTAL_MIN_VALUE = ORDER_CONSTANTS.Limits.SUBTOTAL_MIN_VALUE
TAX_AMOUNT_MAX_VALUE = ORDER_CONSTANTS.Limits.TAX_AMOUNT_MAX_VALUE
TAX_AMOUNT_MIN_VALUE = ORDER_CONSTANTS.Limits.TAX_AMOUNT_MIN_VALUE
TOTAL_MAX_VALUE = ORDER_CONSTANTS.Limits.TOTAL_MAX_VALUE
TOTAL_MIN_VALUE = ORDER_CONSTANTS.Limits.TOTAL_MIN_VALUE
UNITS_MAX_VALUE = ORDER_CONSTANTS.Limits.UNITS_MAX_VALUE
UNITS_MIN_VALUE = ORDER_CONSTANTS.Limits.UNITS_MIN_VALUE


# Secuencia atómica para el número de ordenes de compra
order_number_seq = Sequence(
    name="order_number_seq",
    schema="orders",
    start=1,
    metadata=ModelBase.metadata,
)


class Order(ModelBase):
    """Modelo ORM para la gestión de órdenes/transacciones."""

    __tablename__ = "orders"
    __table_args__ = (
        Index(
            "ix_orders_payment_data_date_joined",
            text(text="(payment_data ->> 'description')"),
            "date_joined",
        ),
        CheckConstraint(
            sqltext=f"subtotal > {SUBTOTAL_MIN_VALUE} AND subtotal <= {SUBTOTAL_MAX_VALUE}",
            name="subtotal_range",
        ),
        CheckConstraint(
            sqltext=f"total > {TOTAL_MIN_VALUE} AND total <= {TOTAL_MAX_VALUE}",
            name="totals_range",
        ),
        CheckConstraint(
            sqltext=f"tax_amount > {TAX_AMOUNT_MIN_VALUE} AND tax_amount <= {TAX_AMOUNT_MAX_VALUE}",
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
        doc=ORDER_CONSTANTS.Docs.IDEMPOTENCY_KEY_DESCRIPTION,
        unique=True,
        nullable=False,
        index=True,
    )
    order_number: Mapped[str] = mapped_column(
        String(length=15),
        doc=ORDER_CONSTANTS.Docs.ORDER_NUMBER_DESCRIPTION,
        unique=True,
        nullable=False,
    )
    customer_data: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        doc=ORDER_CONSTANTS.Docs.CUSTOMER_DATA_DESCRIPTION,
        nullable=True,
    )
    product_data: Mapped[list[dict[str, Any]] | None] = mapped_column(
        JSONB,
        doc=ORDER_CONSTANTS.Docs.PRODUCT_DATA_DESCRIPTION,
        nullable=True,
    )
    payment_data: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        doc=ORDER_CONSTANTS.Docs.PAYMENT_DATA_DESCRIPTION,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(length=100),
        doc=ORDER_CONSTANTS.Docs.STATUS_DESCRIPTION,
        nullable=False,
        index=True,
    )
    status_history: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        doc=ORDER_CONSTANTS.Docs.STATUS_HISTORY_DESCRIPTION,
        nullable=False,
    )
    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=ORDER_CONSTANTS.Limits.SUBTOTAL_MAX_DIGITS,
            scale=ORDER_CONSTANTS.Limits.SUBTOTAL_DECIMAL_PLACES,
            asdecimal=True,
        ),
        doc=ORDER_CONSTANTS.Docs.SUBTOTAL_DESCRIPTION,
        nullable=False,
    )
    total: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=ORDER_CONSTANTS.Limits.TOTAL_MAX_DIGITS,
            scale=ORDER_CONSTANTS.Limits.TOTAL_DECIMAL_PLACES,
            asdecimal=True,
        ),
        doc=ORDER_CONSTANTS.Docs.TOTAL_DESCRIPTION,
        nullable=False,
    )
    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=ORDER_CONSTANTS.Limits.TAX_AMOUNT_MAX_DIGITS,
            scale=ORDER_CONSTANTS.Limits.TAX_AMOUNT_DECIMAL_PLACES,
            asdecimal=True,
        ),
        doc=ORDER_CONSTANTS.Docs.TAX_AMOUNT_DESCRIPTION,
        nullable=False,
    )
    units: Mapped[int] = mapped_column(
        Integer,
        doc=ORDER_CONSTANTS.Docs.UNITS_DESCRIPTION,
        nullable=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
