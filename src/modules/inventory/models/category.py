from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base
from src.modules.inventory.constants import CategoryEntity

# Constantes para validaciones de campos numéricos
MAXIMUM_PRODUCTS = CategoryEntity.MAXIMUM_NUMBER_PRODUCTS.value
MINIMUM_PRODUCTS = CategoryEntity.MINIMUM_NUMBER_PRODUCTS.value


class Category(Base):
    """
    Modelo ORM para la clasificación y categorización de productos en el inventario.

    Define la agrupación lógica de productos en el esquema `product`, gestionando su
    estado operativo, descripción y el conteo acumulado de artículos asociados.
    """

    __tablename__ = "categories"
    __table_args__ = {"schema": "product"}

    id: Mapped[UUID] = mapped_column(
        doc=CategoryEntity.ID_DESCRIPTION.value,
        default=uuid4,
        primary_key=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(length=CategoryEntity.NAME_MAX_LENGTH.value),
        doc=CategoryEntity.NAME_DESCRIPTION.value,
        unique=True,
        nullable=True,
    )
    description: Mapped[str] = mapped_column(
        String(length=CategoryEntity.DESCRIPTION_MAX_LENGTH.value),
        doc=CategoryEntity.DESCRIPTION_DESCRIPTION.value,
        nullable=True,
    )
    product_count: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            sqltext=f"product_count >= {MINIMUM_PRODUCTS} AND product_count <= {MAXIMUM_PRODUCTS}",
            name="product_count_range",
        ),
        doc=CategoryEntity.PRODUCT_NUMBER_DESCRIPTION.value,
        nullable=True,
    )
    status: Mapped[bool] = mapped_column(
        Boolean,
        doc=CategoryEntity.STATUS_DESCRIPTION.value,
        nullable=True,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc=CategoryEntity.DATE_JOINED_DESCRIPTION.value,
        default=lambda: datetime.now(tz=UTC),
        nullable=True,
    )
