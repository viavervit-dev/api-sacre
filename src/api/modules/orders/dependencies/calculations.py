from typing import Annotated

from fastapi import Depends

from src.api.common.utils import FinancialCalculationsMixin


def financial_calculations_service() -> type[FinancialCalculationsMixin]:
    """Dependencia que expone la clase de utilidades para cálculos financieros."""

    return FinancialCalculationsMixin


FinancialCalculationServiceDep = Annotated[
    type[FinancialCalculationsMixin], Depends(financial_calculations_service)
]
