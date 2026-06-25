from decimal import Decimal, InvalidOperation
from typing import Annotated, Any
from uuid import UUID

from fastapi.exceptions import RequestValidationError
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    TypeAdapter,
    field_validator,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.constants import DTOValidationErrorMessages
from src.modules.products.constants import CategoryEntity, ProductEntity, VatRatesProduct
from src.modules.products.repositories.interfaces import IProductRepository

CATEGORY_NAME_MAX_LENGTH = CategoryEntity.NAME_MAX_LENGTH.value
URL_IMAGES_MAX_LENGTH = ProductEntity.URL_IMAGES_MAX_LENGTH.value


class CreateCategoryDTO(BaseModel):
    """DTO para la creación de una categoria de producto."""

    name: str = Field(
        max_length=CategoryEntity.NAME_MAX_LENGTH.value,
        description=CategoryEntity.NAME_DESCRIPTION.value,
        examples=["Rosarios"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                CategoryEntity.NAME_IN_USE.value,
            ]
        },
    )
    description: str = Field(
        max_length=CategoryEntity.DESCRIPTION_MAX_LENGTH.value,
        description=CategoryEntity.DESCRIPTION_DESCRIPTION.value,
        examples=[
            "Descubre nuestra colección de rosarios, elaborados con dedicación y pensados para "
            "acompañarte en cada momento de oración y reflexión. Contamos con una amplia variedad "
            "de diseños que combinan tradición, elegancia y calidad, ideales tanto para uso "
            "personal como para regalo."
        ],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )

    async def check_name(
        self,
        db: AsyncSession,
        product_repo: type[IProductRepository],
    ) -> None:
        """Ejecuta validaciones para el nombre de la categoría."""

        # Validar que el nombre de la categoría no esté registrado en la base de datos
        exists = await product_repo.exists_category(db=db, filters={"name": self.name})

        if exists:
            raise RequestValidationError(
                errors=[
                    {
                        "loc": ("body", "name"),
                        "msg": CategoryEntity.NAME_IN_USE.value,
                        "type": "domain_validation",
                    }
                ]
            )


class UpdateCategoryDTO(BaseModel):
    """DTO para la creación de una categoria de producto."""

    name: str | None = Field(
        max_length=CategoryEntity.NAME_MAX_LENGTH.value,
        description=CategoryEntity.NAME_DESCRIPTION.value,
        default=None,
        examples=["Rosarios"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                CategoryEntity.NAME_IN_USE.value,
            ]
        },
    )
    description: str | None = Field(
        max_length=CategoryEntity.DESCRIPTION_MAX_LENGTH.value,
        description=CategoryEntity.DESCRIPTION_DESCRIPTION.value,
        default=None,
        examples=[
            "Descubre nuestra colección de rosarios, elaborados con dedicación y pensados para "
            "acompañarte en cada momento de oración y reflexión. Contamos con una amplia variedad "
            "de diseños que combinan tradición, elegancia y calidad, ideales tanto para uso "
            "personal como para regalo."
        ],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )

    async def check_name(
        self,
        db: AsyncSession,
        product_repo: type[IProductRepository],
    ) -> None:
        """Ejecuta validaciones para el nombre de la categoría."""

        if not self.name:
            return None

        # Validar que el nombre de la categoría no esté registrado en la base de datos
        exists = await product_repo.exists_category(db=db, filters={"name": self.name})

        if exists:
            raise RequestValidationError(
                errors=[
                    {
                        "loc": ("body", "name"),
                        "msg": CategoryEntity.NAME_IN_USE.value,
                        "type": "domain_validation",
                    }
                ]
            )


class PrivateReadCategoryDTO(BaseModel):
    """
    DTO para la lectura de una categoría de producto con información completa, incluyendo campos
    que solo deberían ser visibles para administradores.
    """

    id: UUID = Field(
        description=CategoryEntity.ID_DESCRIPTION.value,
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    name: str = Field(
        description=CategoryEntity.NAME_DESCRIPTION.value,
        examples=["Rosarios"],
    )
    description: str = Field(
        description=CategoryEntity.DESCRIPTION_DESCRIPTION.value,
        examples=[
            "Descubre nuestra colección de rosarios, elaborados con dedicación y pensados para "
            "acompañarte en cada momento de oración y reflexión. Contamos con una amplia variedad "
            "de diseños que combinan tradición, elegancia y calidad, ideales tanto para uso "
            "personal como para regalo."
        ],
    )
    product_count: int = Field(
        description=CategoryEntity.DESCRIPTION_DESCRIPTION.value,
        examples=[10, 15],
    )
    status: bool = Field(
        description=CategoryEntity.DESCRIPTION_DESCRIPTION.value,
        examples=[True, False],
    )


class PublicReadCategoryDTO(BaseModel):
    """DTO para la lectura de una categoría de producto con información pública."""

    id: UUID = Field(
        description=CategoryEntity.ID_DESCRIPTION.value,
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    name: str = Field(
        description=CategoryEntity.NAME_DESCRIPTION.value,
        examples=["Rosarios"],
    )
    description: str = Field(
        description=CategoryEntity.DESCRIPTION_DESCRIPTION.value,
        examples=[
            "Descubre nuestra colección de rosarios, elaborados con dedicación y pensados para "
            "acompañarte en cada momento de oración y reflexión. Contamos con una amplia variedad "
            "de diseños que combinan tradición, elegancia y calidad, ideales tanto para uso "
            "personal como para regalo."
        ],
    )
    product_count: int = Field(
        description=CategoryEntity.DESCRIPTION_DESCRIPTION.value,
        examples=[10, 15],
    )


class CreateProductDTO(BaseModel):
    """DTO para la creación de un producto."""

    name: str = Field(
        max_length=ProductEntity.NAME_MAX_LENGTH.value,
        description=ProductEntity.NAME_DESCRIPTION.value,
        examples=["Rosario de madera"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                ProductEntity.NAME_IN_USE.value,
            ]
        },
    )
    categories: list[Annotated[str, Field(max_length=CATEGORY_NAME_MAX_LENGTH)]] = Field(
        description=ProductEntity.CATEGORIES_DESCRIPTION.value,
        examples=[["Rosarios", "Madera"]],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                ProductEntity.CATEGORY_NOT_FOUND.value,
            ]
        },
    )
    description_short: str = Field(
        max_length=ProductEntity.DESCRIPTION_SHORT_MAX_LENGTH.value,
        description=ProductEntity.DESCRIPTION_SHORT_DESCRIPTION.value,
        examples=["Rosario hecho a mano con cuentas de madera."],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )
    description_long: str = Field(
        max_length=ProductEntity.DESCRIPTION_LONG_MAX_LENGTH.value,
        description=ProductEntity.DESCRIPTION_LONG_DESCRIPTION.value,
        examples=[
            "Este rosario está fabricado a mano utilizando madera de alta calidad, ideal para "
            "orar en el día a día. Cuenta con un diseño elegante y tradicional."
        ],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )
    images: list[Annotated[str, Field(max_length=URL_IMAGES_MAX_LENGTH)]] = Field(
        min_length=ProductEntity.MINIMUM_NUMBER_IMAGES.value,
        max_length=ProductEntity.MAXIMUM_NUMBER_IMAGES.value,
        description=ProductEntity.IMAGES_DESCRIPTION.value,
        examples=[
            [
                "https://example.com/image1.jpg",
                "https://example.com/image2.jpg",
                "https://example.com/image3.jpg",
            ]
        ],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                ProductEntity.URL_INVALID.value,
            ]
        },
    )
    price_neto: Decimal = Field(
        ge=ProductEntity.PRICE_NETO_MIN_VALUE.value,
        le=ProductEntity.PRICE_NETO_MAX_VALUE.value,
        max_digits=ProductEntity.PRICE_NETO_MAX_DIGITS.value,
        decimal_places=ProductEntity.PRICE_NETO_DECIMAL_PLACES.value,
        description=ProductEntity.PRICE_NETO_DESCRIPTION.value,
        examples=[Decimal("10.50")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN_EQUAL.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES.value,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS.value,
            ]
        },
    )
    profit_margin: Decimal = Field(
        ge=ProductEntity.PROFIT_MARGIN_MIN_VALUE.value,
        le=ProductEntity.PROFIT_MARGIN_MAX_VALUE.value,
        max_digits=ProductEntity.PROFIT_MARGIN_MAX_DIGITS.value,
        decimal_places=ProductEntity.PROFIT_MARGIN_DECIMAL_PLACES.value,
        description=ProductEntity.PROFIT_MARGIN_DESCRIPTION.value,
        examples=[Decimal("0.1600")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN_EQUAL.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES.value,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS.value,
            ]
        },
    )
    iva: VatRatesProduct = Field(
        description=ProductEntity.IVA_DESCRIPTION.value,
        examples=VatRatesProduct.values(),
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.ENUM.value,
            ]
        },
    )
    stock_total: int = Field(
        ge=ProductEntity.STOCK_TOTAL_MIN_VALUE.value,
        le=ProductEntity.STOCK_TOTAL_MAX_VALUE.value,
        description=ProductEntity.STOCK_TOTAL_DESCRIPTION.value,
        examples=[100],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN_EQUAL.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
            ]
        },
    )

    @field_validator("iva", mode="before")
    @classmethod
    def cast_iva_to_decimal(cls, value: Any) -> Any:
        """
        Intercepta el valor de entrada (str o float) y lo convierte a Decimal antes de que
        `Pydantic` valide si pertenece al `Enum`.
        """

        if isinstance(value, (Decimal, VatRatesProduct)):
            return value

        try:
            return Decimal(value=str(value))
        except (InvalidOperation, TypeError, ValueError):
            return value

    async def check_name(
        self,
        db: AsyncSession,
        product_repo: type[IProductRepository],
    ) -> None:
        """Ejecuta validaciones para el nombre del producto."""

        # Validar que el nombre del producto no esté registrado en la base de datos
        exists = await product_repo.exists_product(db=db, filters={"name": self.name})

        if exists:
            raise RequestValidationError(
                errors=[
                    {
                        "loc": ("body", "name"),
                        "msg": ProductEntity.NAME_IN_USE.value,
                        "type": "domain_validation",
                    }
                ]
            )

    async def check_images_urls(
        self,
        db: AsyncSession,
        product_repo: type[IProductRepository],
    ) -> None:
        """Valida que cada elemento de la lista de imágenes sea una URL válida."""

        adapter = TypeAdapter(HttpUrl)
        errors = []

        for i, url in enumerate(self.images):
            try:
                adapter.validate_python(url)
            except Exception:
                errors.append(
                    {
                        "loc": ("body", "images", i),
                        "msg": ProductEntity.URL_INVALID.value,
                        "type": "domain_validation",
                    }
                )

        if errors:
            raise RequestValidationError(errors=errors)

    async def check_categories(
        self,
        db: AsyncSession,
        product_repo: type[IProductRepository],
    ) -> None:
        """Ejecuta validaciones para el campo `categories` del producto."""

        errors = []

        for i, category in enumerate(self.categories):
            exists = await product_repo.exists_category(
                filters={"name": category},
                db=db,
            )

            if not exists:
                errors.append(
                    {
                        "loc": ("body", "categories", i),
                        "msg": ProductEntity.CATEGORY_NOT_FOUND.value,
                        "type": "domain_validation",
                    }
                )

        if errors:
            raise RequestValidationError(errors=errors)


class UpdateProductDTO(BaseModel):
    """DTO para la actualización de un producto."""

    model_config = ConfigDict(use_enum_values=True)

    name: str | None = Field(
        max_length=ProductEntity.NAME_MAX_LENGTH.value,
        description=ProductEntity.NAME_DESCRIPTION.value,
        default=None,
        examples=["Rosario de madera"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                ProductEntity.NAME_IN_USE.value,
            ]
        },
    )
    categories: list[Annotated[str, Field(max_length=CATEGORY_NAME_MAX_LENGTH)]] | None = Field(
        description=ProductEntity.CATEGORIES_DESCRIPTION.value,
        default=None,
        examples=[["Rosarios", "Madera"]],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                ProductEntity.CATEGORY_NOT_FOUND.value,
            ]
        },
    )
    description_short: str | None = Field(
        max_length=ProductEntity.DESCRIPTION_SHORT_MAX_LENGTH.value,
        description=ProductEntity.DESCRIPTION_SHORT_DESCRIPTION.value,
        default=None,
        examples=["Rosario hecho a mano con cuentas de madera."],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )
    description_long: str | None = Field(
        max_length=ProductEntity.DESCRIPTION_LONG_MAX_LENGTH.value,
        description=ProductEntity.DESCRIPTION_LONG_DESCRIPTION.value,
        default=None,
        examples=[
            "Este rosario está fabricado a mano utilizando madera de alta calidad, ideal para "
            "orar en el día a día. Cuenta con un diseño elegante y tradicional."
        ],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )
    images: list[Annotated[str, Field(max_length=URL_IMAGES_MAX_LENGTH)]] | None = Field(
        min_length=ProductEntity.MINIMUM_NUMBER_IMAGES.value,
        max_length=ProductEntity.MAXIMUM_NUMBER_IMAGES.value,
        description=ProductEntity.IMAGES_DESCRIPTION.value,
        default=None,
        examples=[
            [
                "https://example.com/image1.jpg",
                "https://example.com/image2.jpg",
                "https://example.com/image3.jpg",
            ]
        ],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.STRING_TOO_LONG.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                ProductEntity.URL_INVALID.value,
            ]
        },
    )
    price_neto: Decimal | None = Field(
        ge=ProductEntity.PRICE_NETO_MIN_VALUE.value,
        le=ProductEntity.PRICE_NETO_MAX_VALUE.value,
        max_digits=ProductEntity.PRICE_NETO_MAX_DIGITS.value,
        decimal_places=ProductEntity.PRICE_NETO_DECIMAL_PLACES.value,
        description=ProductEntity.PRICE_NETO_DESCRIPTION.value,
        default=None,
        examples=[Decimal("10.55")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN_EQUAL.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES.value,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS.value,
            ]
        },
    )
    profit_margin: Decimal | None = Field(
        ge=ProductEntity.PROFIT_MARGIN_MIN_VALUE.value,
        le=ProductEntity.PROFIT_MARGIN_MAX_VALUE.value,
        max_digits=ProductEntity.PROFIT_MARGIN_MAX_DIGITS.value,
        decimal_places=ProductEntity.PROFIT_MARGIN_DECIMAL_PLACES.value,
        description=ProductEntity.PROFIT_MARGIN_DESCRIPTION.value,
        default=None,
        examples=[Decimal("0.1600")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN_EQUAL.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES.value,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS.value,
            ]
        },
    )
    iva: VatRatesProduct | None = Field(
        description=ProductEntity.IVA_DESCRIPTION.value,
        default=None,
        examples=VatRatesProduct.values(),
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.ENUM.value,
            ]
        },
    )
    stock_total: int | None = Field(
        ge=ProductEntity.STOCK_TOTAL_MIN_VALUE.value,
        le=ProductEntity.STOCK_TOTAL_MAX_VALUE.value,
        description=ProductEntity.STOCK_TOTAL_DESCRIPTION.value,
        default=None,
        examples=[100],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN_EQUAL.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
            ]
        },
    )

    @field_validator("iva", mode="before")
    @classmethod
    def cast_iva_to_decimal(cls, value: Any) -> Any:
        """
        Intercepta el valor de entrada (str o float) y lo convierte a Decimal antes de que
        `Pydantic` valide si pertenece al `Enum`.
        """

        if value is None:
            return None

        if isinstance(value, (Decimal, VatRatesProduct)):
            return value

        try:
            return Decimal(value=str(value))
        except (InvalidOperation, TypeError, ValueError):
            return value

    async def check_name(
        self,
        db: AsyncSession,
        product_repo: type[IProductRepository],
    ) -> None:
        """Ejecuta validaciones para el nombre del producto."""

        if not self.name:
            return None

        # Validar que el nombre del producto no esté registrado en la base de datos
        exists = await product_repo.exists_product(db=db, filters={"name": self.name})

        if exists:
            raise RequestValidationError(
                errors=[
                    {
                        "loc": ("body", "name"),
                        "msg": ProductEntity.NAME_IN_USE.value,
                        "type": "domain_validation",
                    }
                ]
            )

    async def check_images_urls(
        self,
        db: AsyncSession,
        product_repo: type[IProductRepository],
    ) -> None:
        """Valida que cada elemento de la lista de imágenes sea una URL válida."""

        if not self.images:
            return None

        adapter = TypeAdapter(HttpUrl)
        errors = []

        for i, url in enumerate(self.images):
            try:
                adapter.validate_python(url)
            except Exception:
                errors.append(
                    {
                        "loc": ("body", "images", i),
                        "msg": ProductEntity.URL_INVALID.value,
                        "type": "domain_validation",
                    }
                )

        if errors:
            raise RequestValidationError(errors=errors)

    async def check_categories(
        self,
        db: AsyncSession,
        product_repo: type[IProductRepository],
    ) -> None:
        """Ejecuta validaciones para el campo `categories` del producto."""

        if not self.categories:
            return None

        errors = []

        for i, category in enumerate(self.categories):
            exists = await product_repo.exists_category(
                filters={"name": category},
                db=db,
            )

            if not exists:
                errors.append(
                    {
                        "loc": ("body", "categories", i),
                        "msg": ProductEntity.CATEGORY_NOT_FOUND.value,
                        "type": "domain_validation",
                    }
                )

        if errors:
            raise RequestValidationError(errors=errors)


class PrivateReadProductDTO(BaseModel):
    """
    DTO para la lectura de un producto con información completa, incluyendo campos que solo
    deberían ser visibles para administradores.
    """

    id: UUID = Field(
        description=ProductEntity.ID_DESCRIPTION.value,
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    name: str = Field(
        description=ProductEntity.NAME_DESCRIPTION.value,
        examples=["Rosario de madera"],
    )
    categories: list[str] = Field(
        description=ProductEntity.CATEGORIES_DESCRIPTION.value,
        examples=[["Rosarios", "Madera"]],
    )
    description_short: str = Field(
        description=ProductEntity.DESCRIPTION_SHORT_DESCRIPTION.value,
        examples=["Rosario hecho a mano con cuentas de madera."],
    )
    description_long: str = Field(
        description=ProductEntity.DESCRIPTION_LONG_DESCRIPTION.value,
        examples=[
            "Este rosario está fabricado a mano utilizando madera de alta calidad, ideal para "
            "orar en el día a día. Cuenta con un diseño elegante y tradicional."
        ],
    )
    images: list[str] = Field(
        description=ProductEntity.IMAGES_DESCRIPTION.value,
        examples=[
            [
                "https://example.com/image1.jpg",
                "https://example.com/image2.jpg",
                "https://example.com/image3.jpg",
            ]
        ],
    )
    price_neto: Decimal = Field(
        description=ProductEntity.PRICE_NETO_DESCRIPTION.value,
        examples=[Decimal("10.50")],
    )
    price_sale: Decimal = Field(
        description=ProductEntity.PRICE_SALE_DESCRIPTION.value,
        examples=[Decimal("15.00")],
    )
    profit_margin: Decimal = Field(
        description=ProductEntity.PROFIT_MARGIN_DESCRIPTION.value,
        examples=[Decimal("0.16")],
    )
    iva: Decimal = Field(
        description=ProductEntity.IVA_DESCRIPTION.value,
        examples=[Decimal("0.16")],
    )
    stock_total: int = Field(
        description=ProductEntity.STOCK_TOTAL_DESCRIPTION.value,
        examples=[100],
    )
    stock_hand: int = Field(
        description=ProductEntity.STOCK_HAND_DESCRIPTION.value,
        examples=[80],
    )
    stock_sale: int = Field(
        description=ProductEntity.STOCK_SALE_DESCRIPTION.value,
        examples=[20],
    )
    status: bool = Field(
        description=ProductEntity.STATUS_DESCRIPTION.value,
        examples=[True, False],
    )


class PublicReadProductDTO(BaseModel):
    """DTO para la lectura de un producto con información pública."""

    id: UUID = Field(
        description=ProductEntity.ID_DESCRIPTION.value,
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    name: str = Field(
        description=ProductEntity.NAME_DESCRIPTION.value,
        examples=["Rosario de madera"],
    )
    categories: list[str] = Field(
        description=ProductEntity.CATEGORIES_DESCRIPTION.value,
        examples=[["Rosarios", "Madera"]],
    )
    description_short: str = Field(
        description=ProductEntity.DESCRIPTION_SHORT_DESCRIPTION.value,
        examples=["Rosario hecho a mano con cuentas de madera."],
    )
    description_long: str = Field(
        description=ProductEntity.DESCRIPTION_LONG_DESCRIPTION.value,
        examples=[
            "Este rosario está fabricado a mano utilizando madera de alta calidad, ideal para "
            "orar en el día a día. Cuenta con un diseño elegante y tradicional."
        ],
    )
    images: list[str] = Field(
        description=ProductEntity.IMAGES_DESCRIPTION.value,
        examples=[
            [
                "https://example.com/image1.jpg",
                "https://example.com/image2.jpg",
                "https://example.com/image3.jpg",
            ]
        ],
    )
    price_sale: Decimal = Field(
        description=ProductEntity.PRICE_SALE_DESCRIPTION.value,
        examples=[Decimal("15.00")],
    )
    stock_sale: int = Field(
        description=ProductEntity.STOCK_SALE_DESCRIPTION.value,
        examples=[20],
    )
