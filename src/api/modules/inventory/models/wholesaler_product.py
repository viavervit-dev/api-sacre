from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import ARRAY, Boolean, DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from src.api.modules.inventory.constants import CategoryEntity, WholesalerProductEntity
from src.api.settings.database import ModelBase


class WholesalerProduct(ModelBase):
    """Modelo ORM para la gestión de productos de clientes mayoristas del inventario."""

    __tablename__ = "wholesaler_products"
    __table_args__ = (
        Index(
            "ix_wholesaler_products_exclusive_status_date",
            "exclusive",
            "status",
            "date_joined",
        ),
        Index(
            "ix_wholesaler_products_wholesaler_id_status_date",
            "wholesaler_id",
            "status",
            "date_joined",
        ),
        {"schema": "inventory"},
    )

    id: Mapped[UUID] = mapped_column(
        doc="Identificador único (UUID v4).",
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    wholesaler_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="auth.users.id", ondelete="CASCADE"),
        doc="Identificador único del cliente mayorista al que pertenece este producto.",
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(length=WholesalerProductEntity.NAME_MAX_LENGTH.value),
        doc=WholesalerProductEntity.NAME_DESCRIPTION.value,
        nullable=False,
        unique=True,
    )
    categories: Mapped[list[str]] = mapped_column(
        ARRAY(item_type=String(length=CategoryEntity.NAME_MAX_LENGTH.value)),
        doc=WholesalerProductEntity.CATEGORIES_DESCRIPTION.value,
        nullable=False,
    )
    description_short: Mapped[str] = mapped_column(
        String(length=WholesalerProductEntity.DESCRIPTION_SHORT_MAX_LENGTH.value),
        doc=WholesalerProductEntity.DESCRIPTION_SHORT_DESCRIPTION.value,
        nullable=False,
    )
    description_long: Mapped[str] = mapped_column(
        String(length=WholesalerProductEntity.DESCRIPTION_LONG_MAX_LENGTH.value),
        doc=WholesalerProductEntity.DESCRIPTION_LONG_DESCRIPTION.value,
        nullable=False,
    )
    status: Mapped[bool] = mapped_column(
        Boolean,
        doc=WholesalerProductEntity.STATUS_DESCRIPTION.value,
        nullable=False,
    )
    exclusive: Mapped[bool] = mapped_column(
        Boolean,
        doc=WholesalerProductEntity.EXCLUSIVE_DESCRIPTION.value,
        nullable=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc="Fecha y hora de la creación del registro.",
        default=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
