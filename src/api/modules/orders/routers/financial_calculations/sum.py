from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.api.common.response import Response
from src.api.common.schema import response_scheme_400
from src.api.common.utils import FinancialCalculationsMixin
from src.api.modules.orders.dependencies import financial_calculations_service
from src.api.modules.orders.dto import ListDecimalNumberDTO, ReadDecimalNumberDTO

sum_router = APIRouter(prefix="/orders", tags=["Ordenes de Compra"])


@sum_router.post(
    path="/financial_calculations/sum/",
    response_description="**(OK)** Suma de valores decimales calculada exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_400_BAD_REQUEST: response_scheme_400(dto_class=ListDecimalNumberDTO)},
)
async def sum(
    data: ListDecimalNumberDTO,
    service: Annotated[type[FinancialCalculationsMixin], Depends(financial_calculations_service)],
) -> Response[ReadDecimalNumberDTO]:
    """
    Recibe una colección de valores numéricos decimales y realiza su suma aritmética
    empleando precisión monetaria exacta. Aplica redondeo estándar a dos decimales sobre
    el resultado final para garantizar consistencia financiera en operaciones de presupuestos,
    órdenes de compra y facturación.

    ### Requisitos de Acceso
    - **Acceso Público:** Endpoint abierto. No requiere autenticación ni cookies de sesión.

    ### Flujo de Ejecución
    1. **Validación Sintáctica:**
        - Valida que la lista contenga el número permitido de elementos.
        - Comprueba que cada valor decimal cumpla con las restricciones de rango.
    2. **Cálculo Financiero:**
        - Itera sobre los valores provistos o negativos acumulándolos mediante el método `sum` de
         `FinancialCalculationsMixin` con base inicial `Decimal("0.00")`.
        - Cuantiza el total resultante a dos posiciones decimales aplicando redondeo hacia
         arriba en mitades.
    """

    total = service.sum(values=(item for item in data.value))

    return Response(
        success=True,
        pagination=False,
        message="Suma de valores decimales calculada exitosamente.",
        data=ReadDecimalNumberDTO.model_construct(value=total),
    )
