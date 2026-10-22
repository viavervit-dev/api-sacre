from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.api.common.response import Response
from src.api.common.schema import response_scheme_400
from src.api.common.utils import FinancialCalculationsMixin
from src.api.modules.orders.dependencies import financial_calculations_service
from src.api.modules.orders.dto import AddPercentageDTO, ReadDecimalNumberDTO

add_percentage_router = APIRouter(prefix="/orders", tags=["Ordenes de Compra"])


@add_percentage_router.post(
    path="/calculations/add_percentage/",
    response_description="**(OK)** Cálculo de adición porcentual realizado exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_400_BAD_REQUEST: response_scheme_400(dto_class=AddPercentageDTO)},
)
async def add_percentage(
    data: AddPercentageDTO,
    service: Annotated[type[FinancialCalculationsMixin], Depends(financial_calculations_service)],
) -> Response[ReadDecimalNumberDTO]:
    """
    Recibe un monto base y una tasa porcentual en formato decimal y calcula el importe
    total resultante mediante la fórmula `base_value * (1 + percentage)`. Aplica redondeo
    simétrico a dos decimales sobre el resultado final, proporcionando un cálculo financiero
    exacto para recargos, márgenes de intermediación, aranceles o ajustes comerciales.

    ### Requisitos de Acceso
    - **Acceso Público:** Endpoint abierto. No requiere autenticación ni cookies de sesión.

    ### Flujo de Ejecución
    1. **Validación Sintáctica:**
        - Valida que el monto base sea un número decimal positivo.
        - Valida que la tasa porcentual sea un valor decimal positivo.
    2. **Cálculo Financiero:**
        - Aplica el incremento porcentual sobre el monto base y cuantiza el resultado final
         a dos decimales utilizando redondeo hacia arriba en mitades.
    """

    value = service.add_percentage(base_value=data.amount, percentage=data.percentage)

    return Response(
        success=True,
        pagination=False,
        message="Cálculo de adición porcentual realizado exitosamente.",
        data=ReadDecimalNumberDTO.model_construct(value=value),
    )
