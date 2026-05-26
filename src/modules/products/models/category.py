from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer, String
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from src.config.database import Base
from src.modules.products.constants import CategoryEntity

# Constantes para validaciones de campos numéricos
MAXIMUM_PRODUCTS = CategoryEntity.MAXIMUM_NUMBER_PRODUCTS.value
MINIMUM_PRODUCTS = CategoryEntity.MINIMUM_NUMBER_PRODUCTS.value


class Category(MappedAsDataclass, Base):
    """
    Entidad `Category` y modelo ORM de la tabla `categories`. Actúa simultáneamente como entidad de
    dominio y como modelo **SQLAlchemy** para persistencia y migraciones con **Alembic**.
    """

    __tablename__ = "categories"
    __table_args__ = {"schema": "product"}

    name: Mapped[str] = mapped_column(
        String(length=CategoryEntity.NAME_MAX_LENGTH.value),
        doc=CategoryEntity.NAME_DESCRIPTION.value,
        unique=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(length=CategoryEntity.DESCRIPTION_MAX_LENGTH.value),
        doc=CategoryEntity.DESCRIPTION_DESCRIPTION.value,
        nullable=False,
    )
    product_count: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            sqltext=f"product_count >= {MINIMUM_PRODUCTS} AND product_count <= {MAXIMUM_PRODUCTS}",
            name="product_count_range",
        ),
        doc=CategoryEntity.PRODUCT_NUMBER_DESCRIPTION.value,
        nullable=False,
    )
    status: Mapped[bool] = mapped_column(
        Boolean,
        doc=CategoryEntity.STATUS_DESCRIPTION.value,
        nullable=False,
    )
    id: Mapped[UUID] = mapped_column(
        doc=CategoryEntity.ID_DESCRIPTION.value,
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        doc=CategoryEntity.DATE_JOINED_DESCRIPTION.value,
        default_factory=lambda: datetime.now(tz=UTC),
        nullable=False,
    )
