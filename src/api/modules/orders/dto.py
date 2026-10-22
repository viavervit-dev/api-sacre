from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from src.api.common.exceptions import DTOValidationErrorMessages
from src.api.modules.countries.dto import ReadLocationEcuadorDTO
from src.api.modules.inventory.constants import ProductEntity
from src.api.modules.orders.constants import DecimalNumberEntity, OrderEntity
from src.api.modules.users.dto import ReadExtraContactsDTO


class ReadDecimalNumberDTO(BaseModel):
    """DTO para la lectura y respuesta de un valor numérico decimal."""

    value: Decimal = Field(
        description=DecimalNumberEntity.DESCRIPTION.value,
        examples=[Decimal(value="10.50"), Decimal(value="-10.50")],
    )


class ListDecimalNumberDTO(BaseModel):
    """DTO para la entrada de una lista de valores numéricos decimales."""

    value: list[
        Annotated[
            Decimal,
            Field(
                ge=DecimalNumberEntity.MIN_VALUE.value,
                le=DecimalNumberEntity.MAX_VALUE.value,
                max_digits=DecimalNumberEntity.MAX_DIGITS.value,
                decimal_places=DecimalNumberEntity.DECIMAL_PLACES.value,
                description=DecimalNumberEntity.DESCRIPTION.value,
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
            ),
        ]
    ] = Field(
        min_length=DecimalNumberEntity.MIN_LENGTH.value,
        max_length=DecimalNumberEntity.MAX_LENGTH.value,
        description=DecimalNumberEntity.LIST_DESCRIPTION.value,
        examples=[[Decimal(value="100.50"), Decimal(value="-10.50")]],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.MISSING.value,
            ]
        },
    )


class AddPercentageDTO(BaseModel):
    """DTO para el cálculo de adición de un porcentaje a un monto base."""

    amount: Decimal = Field(
        gt=OrderEntity.AMOUNT_MIN_VALUE.value,
        le=OrderEntity.AMOUNT_MAX_VALUE.value,
        max_digits=OrderEntity.AMOUNT_MAX_DIGITS.value,
        decimal_places=OrderEntity.AMOUNT_DECIMAL_PLACES.value,
        description=OrderEntity.AMOUNT_DESCRIPTION.value,
        examples=[Decimal("10.50")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES.value,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS.value,
            ]
        },
    )
    percentage: Decimal = Field(
        gt=OrderEntity.PERCENTAGE_MIN_VALUE.value,
        le=OrderEntity.PERCENTAGE_MAX_VALUE.value,
        max_digits=OrderEntity.PERCENTAGE_MAX_DIGITS.value,
        decimal_places=OrderEntity.PERCENTAGE_DECIMAL_PLACES.value,
        description=OrderEntity.PERCENTAGE_DESCRIPTION.value,
        examples=[Decimal("0.1500")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES.value,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS.value,
            ]
        },
    )


class GetTaxAmountDTO(BaseModel):
    """DTO para el cálculo del monto de impuesto a partir de un monto base."""

    amount: Decimal = Field(
        gt=OrderEntity.AMOUNT_MIN_VALUE.value,
        le=OrderEntity.AMOUNT_MAX_VALUE.value,
        max_digits=OrderEntity.AMOUNT_MAX_DIGITS.value,
        decimal_places=OrderEntity.AMOUNT_DECIMAL_PLACES.value,
        description=OrderEntity.TAX_AMOUNT_DESCRIPTION.value,
        examples=[Decimal("10.50")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES.value,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS.value,
            ]
        },
    )


class MultiplyDecimalDTO(BaseModel):
    """DTO para el cálculo de multiplicación de un valor decimal por un número entero."""

    decimal: Decimal = Field(
        gt=Decimal(value="0.00"),
        le=Decimal(value="999999.99"),
        max_digits=8,
        decimal_places=2,
        description="Valor decimal a multiplicar.",
        examples=[Decimal("10.50")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES.value,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS.value,
            ]
        },
    )
    multiplier: int = Field(
        gt=0,
        le=99999,
        description="Factor multiplicador entero.",
        examples=[150],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
            ]
        },
    )


class ReadCustomerDataDTO(BaseModel):
    """DTO para la lectura de la información del cliente en una orden de compra."""

    id: UUID = Field(
        description="Identificador único (UUID v4).",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    email: str = Field(
        description="Correo electrónico del cliente.",
        examples=["user@email.com"],
    )
    name_or_company_name: str = Field(
        description="Nombre o razón social del cliente.",
        examples=["Juan Pablo", "Parroquia San José de Chaltura"],
    )
    ruc: str | None = Field(
        description="Registro Único de Contribuyentes del cliente.",
        examples=["1790011674001", None],
    )
    phone: str = Field(
        description="Número de teléfono del cliente.",
        examples=["+593 123456789"],
    )
    location: ReadLocationEcuadorDTO = Field(
        description="Datos de ubicación y dirección de entrega.",
    )
    extra_contacts: list[ReadExtraContactsDTO] | None = Field(
        description="Contactos adicionales del cliente.",
        examples=[
            [
                {
                    "country": "Ecuador",
                    "province": "Pichincha",
                    "canton": "Quito",
                    "city": "Zámbiza",
                    "address": "Manzana 12 casa 32",
                }
            ],
            None,
        ],
    )


class ProductDataDTO(BaseModel):
    """DTO para la información del producto en la creación de una orden de compra."""

    id: UUID = Field(
        description="Identificador único (UUID v4).",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.UUID_TYPE.value,
                DTOValidationErrorMessages.UUID_PARSING.value,
                DTOValidationErrorMessages.UUID_VERSION.value,
                OrderEntity.PRODUCT_NOT_FOUND.value,
            ]
        },
    )
    tax_amount: Decimal = Field(
        gt=ProductEntity.TAX_AMOUNT_MIN_VALUE.value,
        le=ProductEntity.TAX_AMOUNT_MAX_VALUE.value,
        max_digits=ProductEntity.TAX_AMOUNT_MAX_DIGITS.value,
        decimal_places=ProductEntity.TAX_AMOUNT_DECIMAL_PLACES.value,
        description=OrderEntity.TAX_AMOUNT_PRODUCT_DESCRIPTION.value,
        examples=[Decimal("10.50")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES.value,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS.value,
                OrderEntity.TAX_AMOUNT_PRODUCT_INVALID.value,
            ]
        },
    )
    subtotal: Decimal = Field(
        gt=OrderEntity.SUBTOTAL_PRODUCT_MIN_VALUE.value,
        le=OrderEntity.SUBTOTAL_PRODUCT_MAX_VALUE.value,
        max_digits=OrderEntity.SUBTOTAL_PRODUCT_MAX_DIGITS.value,
        decimal_places=OrderEntity.SUBTOTAL_PRODUCT_DECIMAL_PLACES.value,
        description=OrderEntity.SUBTOTAL_PRODUCT_DESCRIPTION.value,
        examples=[Decimal("10.50")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES.value,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS.value,
            ]
        },
    )
    total: Decimal = Field(
        gt=OrderEntity.TOTAL_PRODUCT_MIN_VALUE.value,
        le=OrderEntity.TOTAL_PRODUCT_MAX_VALUE.value,
        max_digits=OrderEntity.TOTAL_PRODUCT_MAX_DIGITS.value,
        decimal_places=OrderEntity.TOTAL_PRODUCT_DECIMAL_PLACES.value,
        description=OrderEntity.TOTAL_PRODUCT_DESCRIPTION.value,
        examples=[Decimal("10.50")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES.value,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS.value,
                OrderEntity.TOTAL_PRODUCT_INVALID.value,
            ]
        },
    )
    units: int = Field(
        gt=OrderEntity.UNITS_PRODUCT_MIN_VALUE.value,
        le=OrderEntity.UNITS_PRODUCT_MAX_VALUE.value,
        description=OrderEntity.UNITS_PRODUCT_DESCRIPTION.value,
        examples=[100],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
            ]
        },
    )


class ReadProductDataDTO(BaseModel):
    """DTO para la lectura de la información de los productos de una orden de compra."""

    id: UUID = Field(
        description="Identificador único (UUID v4).",
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
    tax_amount: Decimal = Field(
        description=OrderEntity.TAX_AMOUNT_PRODUCT_DESCRIPTION.value,
        examples=[Decimal("10.50")],
    )
    subtotal: Decimal = Field(
        description=OrderEntity.SUBTOTAL_PRODUCT_DESCRIPTION.value,
        examples=[Decimal("10.50")],
    )
    total: Decimal = Field(
        description=OrderEntity.TOTAL_PRODUCT_DESCRIPTION.value,
        examples=[Decimal("10.50")],
    )
    units: int = Field(
        description=OrderEntity.UNITS_PRODUCT_DESCRIPTION.value,
        examples=[100],
    )


class CreateOrderDTO(BaseModel):
    """DTO para la creación de una orden de compra."""

    order_number: UUID = Field(
        description=OrderEntity.ORDER_NUMBER_DESCRIPTION.value,
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.UUID_TYPE.value,
                DTOValidationErrorMessages.UUID_PARSING.value,
                DTOValidationErrorMessages.UUID_VERSION.value,
                OrderEntity.ORDER_NUMBER_EXISTS.value,
            ]
        },
    )
    product_data: list[ProductDataDTO] = Field(
        min_length=OrderEntity.PRODUCTS_MIN_LENGTH.value,
        max_length=OrderEntity.PRODUCTS_MAX_LENGTH.value,
        description=OrderEntity.PRODUCT_DATA_DESCRIPTION.value,
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
            ]
        },
    )
    units: int = Field(
        gt=OrderEntity.UNITS_MIN_VALUE.value,
        le=OrderEntity.UNITS_MAX_VALUE.value,
        description=OrderEntity.UNITS_DESCRIPTION.value,
        examples=[100],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
                OrderEntity.UNITS_INVALID.value,
            ]
        },
    )
    tax_amount: Decimal = Field(
        gt=OrderEntity.TAX_AMOUNT_MIN_VALUE.value,
        le=OrderEntity.TAX_AMOUNT_MAX_VALUE.value,
        max_digits=OrderEntity.TAX_AMOUNT_MAX_DIGITS.value,
        decimal_places=OrderEntity.TAX_AMOUNT_DECIMAL_PLACES.value,
        description=OrderEntity.TAX_AMOUNT_DESCRIPTION.value,
        examples=[Decimal("10.50")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES.value,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS.value,
                OrderEntity.TAX_AMOUNT_INVALID.value,
            ]
        },
    )
    subtotal: Decimal = Field(
        gt=OrderEntity.SUBTOTAL_MIN_VALUE.value,
        le=OrderEntity.SUBTOTAL_MAX_VALUE.value,
        max_digits=OrderEntity.SUBTOTAL_MAX_DIGITS.value,
        decimal_places=OrderEntity.SUBTOTAL_DECIMAL_PLACES.value,
        description=OrderEntity.SUBTOTAL_DESCRIPTION.value,
        examples=[Decimal("10.50")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES.value,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS.value,
                OrderEntity.SUBTOTAL_INVALID.value,
            ]
        },
    )
    total: Decimal = Field(
        gt=OrderEntity.TOTAL_MIN_VALUE.value,
        le=OrderEntity.TOTAL_MAX_VALUE.value,
        max_digits=OrderEntity.TOTAL_MAX_DIGITS.value,
        decimal_places=OrderEntity.TOTAL_DECIMAL_PLACES.value,
        description=OrderEntity.TOTAL_DESCRIPTION.value,
        examples=[Decimal("10.50")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN.value,
                DTOValidationErrorMessages.VALUE_ERROR.value,
                DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
                DTOValidationErrorMessages.MISSING.value,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES.value,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS.value,
                OrderEntity.TOTAL_INVALID.value,
            ]
        },
    )


class ReadOrderDTO(BaseModel):
    """DTO para la lectura de la información de una orden de compra."""

    id: UUID = Field(
        description="Identificador único (UUID v4).",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    order_number: UUID = Field(
        description=OrderEntity.ORDER_NUMBER_DESCRIPTION.value,
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    customer_data: ReadCustomerDataDTO = Field(
        description=OrderEntity.CUSTOMER_DATA_DESCRIPTION.value,
    )
    product_data: list[ReadProductDataDTO] = Field(
        description=OrderEntity.PRODUCT_DATA_DESCRIPTION.value,
    )
    units: int = Field(
        description=OrderEntity.UNITS_DESCRIPTION.value,
        examples=[100],
    )
    tax_amount: Decimal = Field(
        description=OrderEntity.TAX_AMOUNT_DESCRIPTION.value,
        examples=[Decimal("10.50")],
    )
    subtotal: Decimal = Field(
        description=OrderEntity.SUBTOTAL_DESCRIPTION.value,
        examples=[Decimal("10.50")],
    )
    total: Decimal = Field(
        description=OrderEntity.TOTAL_DESCRIPTION.value,
        examples=[Decimal("10.50")],
    )
