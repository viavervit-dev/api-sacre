from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field

from src.api.common.exceptions import DTOValidationErrorMessages
from src.api.modules.orders.constants.calculations import DECIMAL_NUMBER_CONSTANTS
from src.api.modules.orders.constants.purchase import ORDER_CONSTANTS


class ReadDecimalNumberDTO(BaseModel):
    """Esquema de salida con el valor decimal resultante de un cálculo."""

    value: Decimal = Field(
        description=DECIMAL_NUMBER_CONSTANTS.Docs.DESCRIPTION,
        examples=[Decimal(value="10.50"), Decimal(value="-10.50")],
    )


class ListDecimalNumberDTO(BaseModel):
    """Esquema de entrada para validar una lista de valores decimales a operar."""

    value: list[
        Annotated[
            Decimal,
            Field(
                ge=DECIMAL_NUMBER_CONSTANTS.Limits.MIN_VALUE,
                le=DECIMAL_NUMBER_CONSTANTS.Limits.MAX_VALUE,
                max_digits=DECIMAL_NUMBER_CONSTANTS.Limits.MAX_DIGITS,
                decimal_places=DECIMAL_NUMBER_CONSTANTS.Limits.DECIMAL_PLACES,
                description=DECIMAL_NUMBER_CONSTANTS.Docs.DESCRIPTION,
                json_schema_extra={
                    "x-validation-errors": [
                        DTOValidationErrorMessages.GREATER_THAN_EQUAL,
                        DTOValidationErrorMessages.VALUE_ERROR,
                        DTOValidationErrorMessages.LESS_THAN_EQUAL,
                        DTOValidationErrorMessages.MISSING,
                        DTOValidationErrorMessages.DECIMAL_MAX_PLACES,
                        DTOValidationErrorMessages.DECIMAL_MAX_DIGITS,
                    ]
                },
            ),
        ]
    ] = Field(
        min_length=DECIMAL_NUMBER_CONSTANTS.Limits.MIN_LENGTH,
        max_length=DECIMAL_NUMBER_CONSTANTS.Limits.MAX_LENGTH,
        description=DECIMAL_NUMBER_CONSTANTS.Docs.LIST_DESCRIPTION,
        examples=[[Decimal(value="100.50"), Decimal(value="-10.50")]],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.VALUE_ERROR,
                DTOValidationErrorMessages.MISSING,
            ]
        },
    )


class AddPercentageDTO(BaseModel):
    """Esquema de entrada para validar el cálculo de incremento porcentual sobre un monto."""

    amount: Decimal = Field(
        gt=ORDER_CONSTANTS.Limits.AMOUNT_MIN_VALUE,
        le=ORDER_CONSTANTS.Limits.AMOUNT_MAX_VALUE,
        max_digits=ORDER_CONSTANTS.Limits.AMOUNT_MAX_DIGITS,
        decimal_places=ORDER_CONSTANTS.Limits.AMOUNT_DECIMAL_PLACES,
        description=ORDER_CONSTANTS.Docs.AMOUNT_DESCRIPTION,
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
    percentage: Decimal = Field(
        gt=ORDER_CONSTANTS.Limits.PERCENTAGE_MIN_VALUE,
        le=ORDER_CONSTANTS.Limits.PERCENTAGE_MAX_VALUE,
        max_digits=ORDER_CONSTANTS.Limits.PERCENTAGE_MAX_DIGITS,
        decimal_places=ORDER_CONSTANTS.Limits.PERCENTAGE_DECIMAL_PLACES,
        description=ORDER_CONSTANTS.Docs.PERCENTAGE_DESCRIPTION,
        examples=[Decimal("0.1500")],
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


class GetTaxAmountDTO(BaseModel):
    """Esquema de entrada para validar el monto base en el cálculo de impuestos."""

    amount: Decimal = Field(
        gt=ORDER_CONSTANTS.Limits.AMOUNT_MIN_VALUE,
        le=ORDER_CONSTANTS.Limits.AMOUNT_MAX_VALUE,
        max_digits=ORDER_CONSTANTS.Limits.AMOUNT_MAX_DIGITS,
        decimal_places=ORDER_CONSTANTS.Limits.AMOUNT_DECIMAL_PLACES,
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
            ]
        },
    )


class MultiplyDecimalDTO(BaseModel):
    """
    Esquema de entrada para validar la multiplicación de un monto decimal por una cantidad entera.
    """

    decimal: Decimal = Field(
        gt=Decimal(value="0.00"),
        le=Decimal(value="999999.99"),
        max_digits=8,
        decimal_places=2,
        description="Valor decimal a multiplicar.",
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
    multiplier: int = Field(
        gt=0,
        le=99999,
        description="Factor multiplicador entero.",
        examples=[150],
        json_schema_extra={
            "x-validation-errors": [
                DTOValidationErrorMessages.GREATER_THAN,
                DTOValidationErrorMessages.VALUE_ERROR,
                DTOValidationErrorMessages.LESS_THAN_EQUAL,
                DTOValidationErrorMessages.MISSING,
            ]
        },
    )
