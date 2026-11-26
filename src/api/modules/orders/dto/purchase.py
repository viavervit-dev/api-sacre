from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from src.api.common.exceptions import DTOValidationErrorMessages
from src.api.modules.countries.dto import ReadLocationEcuadorDTO
from src.api.modules.inventory.constants import ProductEntity
from src.api.modules.orders.constants.purchase import (
    ORDER_CONSTANTS,
    OrderDescription,
    OrderStatus,
)
from src.api.modules.users.dto.wholesaler import ReadExtraContactsDTO


class ReadCustomerDataDTO(BaseModel):
    """Esquema de salida con los datos completos del cliente asociados a una orden."""

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
    """Esquema de entrada para validar cada línea de producto al registrar una orden."""

    id: UUID = Field(
        description="Identificador único (UUID v4).",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
                DTOValidationErrorMessages.UUID_TYPE,
                DTOValidationErrorMessages.UUID_PARSING,
                DTOValidationErrorMessages.UUID_VERSION,
                ORDER_CONSTANTS.Errors.PRODUCT_NOT_FOUND,
            ]
        },
    )
    tax_amount: Decimal = Field(
        gt=ProductEntity.TAX_AMOUNT_MIN_VALUE.value,
        le=ProductEntity.TAX_AMOUNT_MAX_VALUE.value,
        max_digits=ProductEntity.TAX_AMOUNT_MAX_DIGITS.value,
        decimal_places=ProductEntity.TAX_AMOUNT_DECIMAL_PLACES.value,
        description=ORDER_CONSTANTS.Docs.TAX_AMOUNT_PRODUCT_DESCRIPTION,
        examples=[Decimal("10.50")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN,
                DTOValidationErrorMessages.VALUE_ERROR,
                DTOValidationErrorMessages.LESS_THAN_EQUAL,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS,
                ORDER_CONSTANTS.Errors.TAX_AMOUNT_PRODUCT_INVALID,
            ]
        },
    )
    subtotal: Decimal = Field(
        gt=ORDER_CONSTANTS.Limits.SUBTOTAL_PRODUCT_MIN_VALUE,
        le=ORDER_CONSTANTS.Limits.SUBTOTAL_PRODUCT_MAX_VALUE,
        max_digits=ORDER_CONSTANTS.Limits.SUBTOTAL_PRODUCT_MAX_DIGITS,
        decimal_places=ORDER_CONSTANTS.Limits.SUBTOTAL_PRODUCT_DECIMAL_PLACES,
        description=ORDER_CONSTANTS.Docs.SUBTOTAL_PRODUCT_DESCRIPTION,
        examples=[Decimal("10.50")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN,
                DTOValidationErrorMessages.VALUE_ERROR,
                DTOValidationErrorMessages.LESS_THAN_EQUAL,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS,
            ]
        },
    )
    total: Decimal = Field(
        gt=ORDER_CONSTANTS.Limits.TOTAL_PRODUCT_MIN_VALUE,
        le=ORDER_CONSTANTS.Limits.TOTAL_PRODUCT_MAX_VALUE,
        max_digits=ORDER_CONSTANTS.Limits.TOTAL_PRODUCT_MAX_DIGITS,
        decimal_places=ORDER_CONSTANTS.Limits.TOTAL_PRODUCT_DECIMAL_PLACES,
        description=ORDER_CONSTANTS.Docs.TOTAL_PRODUCT_DESCRIPTION,
        examples=[Decimal("10.50")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN,
                DTOValidationErrorMessages.VALUE_ERROR,
                DTOValidationErrorMessages.LESS_THAN_EQUAL,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS,
                ORDER_CONSTANTS.Errors.TOTAL_PRODUCT_INVALID,
            ]
        },
    )
    units: int = Field(
        gt=ORDER_CONSTANTS.Limits.UNITS_PRODUCT_MIN_VALUE,
        le=ORDER_CONSTANTS.Limits.UNITS_PRODUCT_MAX_VALUE,
        description=ORDER_CONSTANTS.Docs.UNITS_PRODUCT_DESCRIPTION,
        examples=[100],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN,
                DTOValidationErrorMessages.VALUE_ERROR,
                DTOValidationErrorMessages.LESS_THAN_EQUAL,
                DTOValidationErrorMessages.MISSING,
            ]
        },
    )


class ReadProductDataDTO(BaseModel):
    """Esquema de salida con el detalle de cada producto incluido en una orden."""

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
        description=ORDER_CONSTANTS.Docs.TAX_AMOUNT_PRODUCT_DESCRIPTION,
        examples=[Decimal("10.50")],
    )
    subtotal: Decimal = Field(
        description=ORDER_CONSTANTS.Docs.SUBTOTAL_PRODUCT_DESCRIPTION,
        examples=[Decimal("10.50")],
    )
    total: Decimal = Field(
        description=ORDER_CONSTANTS.Docs.TOTAL_PRODUCT_DESCRIPTION,
        examples=[Decimal("10.50")],
    )
    units: int = Field(
        description=ORDER_CONSTANTS.Docs.UNITS_PRODUCT_DESCRIPTION,
        examples=[100],
    )


class CreateOrderDTO(BaseModel):
    """Esquema de entrada para validar los datos y totales requeridos al crear una orden."""

    idempotency_key: UUID = Field(
        description=ORDER_CONSTANTS.Docs.IDEMPOTENCY_KEY_DESCRIPTION,
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
                DTOValidationErrorMessages.UUID_TYPE,
                DTOValidationErrorMessages.UUID_PARSING,
                DTOValidationErrorMessages.UUID_VERSION,
                ORDER_CONSTANTS.Errors.IDEMPOTENCY_KEY_EXISTS,
            ]
        },
    )
    product_data: list[ProductDataDTO] = Field(
        min_length=ORDER_CONSTANTS.Limits.PRODUCTS_MIN_LENGTH,
        max_length=ORDER_CONSTANTS.Limits.PRODUCTS_MAX_LENGTH,
        description=ORDER_CONSTANTS.Docs.PRODUCT_DATA_DESCRIPTION,
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.VALUE_ERROR,
            ]
        },
    )
    units: int = Field(
        gt=ORDER_CONSTANTS.Limits.UNITS_MIN_VALUE,
        le=ORDER_CONSTANTS.Limits.UNITS_MAX_VALUE,
        description=ORDER_CONSTANTS.Docs.UNITS_DESCRIPTION,
        examples=[100],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN,
                DTOValidationErrorMessages.VALUE_ERROR,
                DTOValidationErrorMessages.LESS_THAN_EQUAL,
                DTOValidationErrorMessages.MISSING,
                ORDER_CONSTANTS.Errors.UNITS_INVALID,
            ]
        },
    )
    tax_amount: Decimal = Field(
        gt=ORDER_CONSTANTS.Limits.TAX_AMOUNT_MIN_VALUE,
        le=ORDER_CONSTANTS.Limits.TAX_AMOUNT_MAX_VALUE,
        max_digits=ORDER_CONSTANTS.Limits.TAX_AMOUNT_MAX_DIGITS,
        decimal_places=ORDER_CONSTANTS.Limits.TAX_AMOUNT_DECIMAL_PLACES,
        description=ORDER_CONSTANTS.Docs.TAX_AMOUNT_DESCRIPTION,
        examples=[Decimal("10.50")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN,
                DTOValidationErrorMessages.VALUE_ERROR,
                DTOValidationErrorMessages.LESS_THAN_EQUAL,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS,
                ORDER_CONSTANTS.Errors.TAX_AMOUNT_INVALID,
            ]
        },
    )
    subtotal: Decimal = Field(
        gt=ORDER_CONSTANTS.Limits.SUBTOTAL_MIN_VALUE,
        le=ORDER_CONSTANTS.Limits.SUBTOTAL_MAX_VALUE,
        max_digits=ORDER_CONSTANTS.Limits.SUBTOTAL_MAX_DIGITS,
        decimal_places=ORDER_CONSTANTS.Limits.SUBTOTAL_DECIMAL_PLACES,
        description=ORDER_CONSTANTS.Docs.SUBTOTAL_DESCRIPTION,
        examples=[Decimal("10.50")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN,
                DTOValidationErrorMessages.VALUE_ERROR,
                DTOValidationErrorMessages.LESS_THAN_EQUAL,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS,
                ORDER_CONSTANTS.Errors.SUBTOTAL_INVALID,
            ]
        },
    )
    total: Decimal = Field(
        gt=ORDER_CONSTANTS.Limits.TOTAL_MIN_VALUE,
        le=ORDER_CONSTANTS.Limits.TOTAL_MAX_VALUE,
        max_digits=ORDER_CONSTANTS.Limits.TOTAL_MAX_DIGITS,
        decimal_places=ORDER_CONSTANTS.Limits.TOTAL_DECIMAL_PLACES,
        description=ORDER_CONSTANTS.Docs.TOTAL_DESCRIPTION,
        examples=[Decimal("10.50")],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN,
                DTOValidationErrorMessages.VALUE_ERROR,
                DTOValidationErrorMessages.LESS_THAN_EQUAL,
                DTOValidationErrorMessages.MISSING,
                DTOValidationErrorMessages.DECIMAL_MAX_PLACES,
                DTOValidationErrorMessages.DECIMAL_MAX_DIGITS,
                ORDER_CONSTANTS.Errors.TOTAL_INVALID,
            ]
        },
    )


class ReadPaymentDataDTO(BaseModel):
    """Esquema de salida con los datos de pago vinculados a una orden."""

    description: str = Field(
        description="Breve descripción del propósito de la órden/transaccións.",
        examples=OrderDescription.values(),
    )
    link: str | None = Field(
        description="Link de pago de la órden/transaccións.",
        examples=["https://ppls.me/rvzpDIGpvT2Fb1y4dx9aYQ", None],
    )


class ReadOrderDTO(BaseModel):
    """Esquema de salida con el detalle completo de una orden registrada."""

    id: UUID = Field(
        description="Identificador único (UUID v4).",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    order_number: str = Field(
        description=ORDER_CONSTANTS.Docs.ORDER_NUMBER_DESCRIPTION,
        examples=["ORD-2026-000001"],
    )
    customer_data: ReadCustomerDataDTO = Field(
        description=ORDER_CONSTANTS.Docs.CUSTOMER_DATA_DESCRIPTION,
    )
    product_data: list[ReadProductDataDTO] = Field(
        description=ORDER_CONSTANTS.Docs.PRODUCT_DATA_DESCRIPTION,
    )
    payment_data: ReadPaymentDataDTO = Field(
        description=ORDER_CONSTANTS.Docs.PAYMENT_DATA_DESCRIPTION,
    )
    units: int = Field(
        description=ORDER_CONSTANTS.Docs.UNITS_DESCRIPTION,
        examples=[100],
    )
    tax_amount: Decimal = Field(
        description=ORDER_CONSTANTS.Docs.TAX_AMOUNT_DESCRIPTION,
        examples=[Decimal("10.50")],
    )
    subtotal: Decimal = Field(
        description=ORDER_CONSTANTS.Docs.SUBTOTAL_DESCRIPTION,
        examples=[Decimal("10.50")],
    )
    total: Decimal = Field(
        description=ORDER_CONSTANTS.Docs.TOTAL_DESCRIPTION,
        examples=[Decimal("10.50")],
    )
    status: str = Field(
        description=ORDER_CONSTANTS.Docs.STATUS_DESCRIPTION,
        examples=OrderStatus.values(),
    )
    status_history: dict[str, Any] = Field(
        description=ORDER_CONSTANTS.Docs.STATUS_HISTORY_DESCRIPTION,
        examples=[
            {
                OrderStatus.PENDING_PAYMENT.value: "2026-10-23T17:25:41.776689+00:00",
                OrderStatus.PAID.value: "2026-10-24T17:25:41.776689+00:00",
            }
        ],
    )
    date_joined: datetime = Field(
        description="Fecha y hora de creación de la orden/transacción.",
        examples=["2026-10-24T17:25:41.776689+00:00"],
    )


class ReadCustomerDataSummaryDTO(BaseModel):
    """Esquema de salida con los datos básicos del cliente para listados de órdenes."""

    id: UUID = Field(
        description="Identificador único (UUID v4).",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    name_or_company_name: str = Field(
        description="Nombre o razón social del cliente.",
        examples=["Juan Pablo", "Parroquia San José de Chaltura"],
    )
    ruc: str | None = Field(
        description="Registro Único de Contribuyentes del cliente.",
        examples=["1790011674001", None],
    )


class ReadOrderSummaryDTO(BaseModel):
    """Esquema de salida con la vista resumida de una orden para listados paginados."""

    id: UUID = Field(
        description="Identificador único (UUID v4).",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    order_number: str = Field(
        description=ORDER_CONSTANTS.Docs.ORDER_NUMBER_DESCRIPTION,
        examples=["ORD-2026-000001"],
    )
    customer_data: ReadCustomerDataSummaryDTO = Field(
        description=ORDER_CONSTANTS.Docs.CUSTOMER_DATA_DESCRIPTION,
    )
    payment_data: ReadPaymentDataDTO = Field(
        description=ORDER_CONSTANTS.Docs.PAYMENT_DATA_DESCRIPTION,
    )
    units: int = Field(
        description=ORDER_CONSTANTS.Docs.UNITS_DESCRIPTION,
        examples=[100],
    )
    total: Decimal = Field(
        description=ORDER_CONSTANTS.Docs.TOTAL_DESCRIPTION,
        examples=[Decimal("10.50")],
    )
    status: str = Field(
        description=ORDER_CONSTANTS.Docs.STATUS_DESCRIPTION,
        examples=OrderStatus.values(),
    )
    date_joined: datetime = Field(
        description="Fecha y hora de creación de la orden/transacción.",
        examples=["2026-10-24T17:25:41.776689+00:00"],
    )
