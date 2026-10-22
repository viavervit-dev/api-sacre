from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.api.common.response import Response
from src.api.common.schema import response_scheme_400
from src.api.common.utils import FinancialCalculationsMixin
from src.api.modules.orders.dependencies import financial_calculations_service
from src.api.modules.orders.dto import MultiplyDecimalDTO, ReadDecimalNumberDTO

multiply_router = APIRouter(prefix="/orders", tags=["Ordenes de Compra"])


@multiply_router.post(
    path="/calculations/multiply/",
    response_description="**(OK)** Multiplicación de valor decimal calculada exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_400_BAD_REQUEST: response_scheme_400(dto_class=MultiplyDecimalDTO)},
)
async def multiply(
    data: MultiplyDecimalDTO,
    service: Annotated[type[FinancialCalculationsMixin], Depends(financial_calculations_service)],
) -> Response[ReadDecimalNumberDTO]:
    """
    Recibe un valor monetario decimal y un factor multiplicador entero, calculando el importe
    total resultante con precisión decimal exacta. Aplica redondeo estándar simétrico a dos
    decimales sobre el producto final para garantizar exactitud y consistencia financiera en
    el cálculo de subtotales por cantidad de unidades en órdenes de compra.

    ### Requisitos de Acceso
    - **Acceso Público:** Endpoint abierto. No requiere autenticación ni cookies de sesión.

    ### Flujo de Ejecución
    1. **Validación Sintáctica:**
        - Valida que el valor decimal sea un número positivo mayor.
        - Valida que el factor multiplicador sea un entero positivo.
    2. **Cálculo Financiero:**
        - Multiplica el valor decimal por el multiplicador entero provisto.
        - Cuantiza el producto resultante a dos posiciones decimales aplicando redondeo hacia
          arriba en mitades.
    """

    value = service.multiply(value=data.decimal, multiplier=data.multiplier)

    return Response(
        success=True,
        pagination=False,
        message="Multiplicación de valor decimal calculada exitosamente.",
        data=ReadDecimalNumberDTO.model_construct(value=value),
    )
