from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import (
    ARRAY,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base
from src.modules.inventory.constants import CategoryEntity, ProductEntity

# Constantes para validaciones de campos numéricos
PRICE_NETO_MAX = ProductEntity.PRICE_NETO_MAX_VALUE.value
PRICE_NETO_MIN = ProductEntity.PRICE_NETO_MIN_VALUE.value
PRICE_SALE_MAX = ProductEntity.PRICE_SALE_MAX_VALUE.value
PRICE_SALE_MIN = ProductEntity.PRICE_SALE_MIN_VALUE.value
PROFIT_MAX = ProductEntity.PROFIT_MARGIN_MAX_VALUE.value
PROFIT_MIN = ProductEntity.PROFIT_MARGIN_MIN_VALUE.value
IVA_MAX = ProductEntity.IVA_MAX_VALUE.value
IVA_MIN = ProductEntity.IVA_MIN_VALUE.value
STOCK_TOTAL_MAX = ProductEntity.STOCK_TOTAL_MAX_VALUE.value
STOCK_TOTAL_MIN = ProductEntity.STOCK_TOTAL_MIN_VALUE.value
STOCK_HAND_MAX = ProductEntity.STOCK_HAND_MAX_VALUE.value
STOCK_HAND_MIN = ProductEntity.STOCK_HAND_MIN_VALUE.value
STOCK_SALE_MAX = ProductEntity.STOCK_SALE_MAX_VALUE.value
STOCK_SALE_MIN = ProductEntity.STOCK_SALE_MIN_VALUE.value


class Product(Base):
    """
    Modelo ORM para la gestión de productos y artículos del inventario.

    Centraliza la información de catálogo, categorización, precios, cálculo de
    márgenes e IVA, y el control de existencias en almacén y venta (`inventory.products`).
    """

    __tablename__ = "products"
    __table_args__ = {"schema": "inventory"}

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    wholesaler_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(column="users.customer_wholesale.id", ondelete="CASCADE"),
        doc="ID del cliente mayorista al que se le vende el producto.",
        nullable=True,
    )
    name: Mapped[str] = mapped_column(
        String(length=ProductEntity.NAME_MAX_LENGTH.value),
        doc=ProductEntity.NAME_DESCRIPTION.value,
        nullable=False,
        unique=True,
    )
    categories: Mapped[list[str]] = mapped_column(
        ARRAY(item_type=String(length=CategoryEntity.NAME_MAX_LENGTH.value)),
        doc=ProductEntity.CATEGORIES_DESCRIPTION.value,
        nullable=False,
    )
    description_short: Mapped[str] = mapped_column(
        String(length=ProductEntity.DESCRIPTION_SHORT_MAX_LENGTH.value),
        doc=ProductEntity.DESCRIPTION_SHORT_DESCRIPTION.value,
        nullable=False,
    )
    description_long: Mapped[str] = mapped_column(
        String(length=ProductEntity.DESCRIPTION_LONG_MAX_LENGTH.value),
        doc=ProductEntity.DESCRIPTION_LONG_DESCRIPTION.value,
        nullable=False,
    )
    images: Mapped[list[str]] = mapped_column(
        ARRAY(item_type=String(length=ProductEntity.URL_IMAGES_MAX_LENGTH.value)),
        doc=ProductEntity.IMAGES_DESCRIPTION.value,
        nullable=False,
    )
    price_neto: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=ProductEntity.PRICE_NETO_MAX_DIGITS.value,
            scale=ProductEntity.PRICE_NETO_DECIMAL_PLACES.value,
            asdecimal=True,
        ),
        CheckConstraint(
            sqltext=f"price_neto >= {PRICE_NETO_MIN} AND price_neto <= {PRICE_NETO_MAX}",
            name="price_neto_range",
        ),
        doc=ProductEntity.PRICE_NETO_DESCRIPTION.value,
        nullable=False,
    )
    price_sale: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=ProductEntity.PRICE_SALE_MAX_DIGITS.value,
            scale=ProductEntity.PRICE_SALE_DECIMAL_PLACES.value,
            asdecimal=True,
        ),
        CheckConstraint(
            sqltext=f"price_sale >= {PRICE_SALE_MIN} AND price_sale <= {PRICE_SALE_MAX}",
            name="price_sale_range",
        ),
        doc=ProductEntity.PRICE_SALE_DESCRIPTION.value,
        nullable=False,
    )
    profit_margin: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=ProductEntity.PROFIT_MARGIN_MAX_DIGITS.value,
            scale=ProductEntity.PROFIT_MARGIN_DECIMAL_PLACES.value,
            asdecimal=True,
        ),
        CheckConstraint(
            sqltext=f"profit_margin >= {PROFIT_MIN} AND profit_margin <= {PROFIT_MAX}",
            name="profit_margin_range",
        ),
        doc=ProductEntity.PROFIT_MARGIN_DESCRIPTION.value,
        nullable=False,
    )
    iva: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=ProductEntity.IVA_MAX_DIGITS.value,
            scale=ProductEntity.IVA_DECIMAL_PLACES.value,
            asdecimal=True,
        ),
        CheckConstraint(
            sqltext=f"iva >= {IVA_MIN} AND iva <= {IVA_MAX}",
            name="iva_range",
        ),
        doc=ProductEntity.IVA_DESCRIPTION.value,
        nullable=False,
    )
    stock_total: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            sqltext=f"stock_total >= {STOCK_TOTAL_MIN} AND stock_total <= {STOCK_TOTAL_MAX}",
            name="stock_total_range",
        ),
        doc=ProductEntity.STOCK_TOTAL_DESCRIPTION.value,
        nullable=False,
    )
    stock_hand: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            sqltext=f"stock_hand >= {STOCK_HAND_MIN} AND stock_hand <= {STOCK_HAND_MAX}",
            name="stock_hand_range",
        ),
        doc=ProductEntity.STOCK_HAND_DESCRIPTION.value,
        nullable=False,
    )
    stock_sale: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            sqltext=f"stock_sale >= {STOCK_SALE_MIN} AND stock_sale <= {STOCK_SALE_MAX}",
            name="stock_sale_range",
        ),
        doc=ProductEntity.STOCK_SALE_DESCRIPTION.value,
        nullable=False,
    )
    status: Mapped[bool] = mapped_column(
        Boolean,
        doc=ProductEntity.STATUS_DESCRIPTION.value,
        nullable=False,
        index=True,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
