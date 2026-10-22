from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.api.common.response import Response
from src.api.common.schema import response_scheme_400
from src.api.common.utils import FinancialCalculationsMixin
from src.api.modules.orders.dependencies import financial_calculations_service
from src.api.modules.orders.dto import GetTaxAmountDTO, ReadDecimalNumberDTO

get_tax_amount_router = APIRouter(prefix="/orders", tags=["Ordenes de Compra"])


@get_tax_amount_router.post(
    path="/calculations/get_tax_amount/",
    response_description="**(OK)** Monto del impuesto calculado exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_400_BAD_REQUEST: response_scheme_400(dto_class=GetTaxAmountDTO)},
)
async def get_tax_amount(
    data: GetTaxAmountDTO,
    service: Annotated[type[FinancialCalculationsMixin], Depends(financial_calculations_service)],
) -> Response[ReadDecimalNumberDTO]:
    """
    Recibe un monto base y calcula el valor correspondiente al impuesto al valor agregado
    (IVA vigente del 15%) aplicando precisión monetaria exacta. Aplica redondeo estándar a
    dos decimales sobre el resultado final para garantizar consistencia y exactitud fiscal
    en cotizaciones y órdenes de compra.

    ### Requisitos de Acceso
    - **Acceso Público:** Endpoint abierto. No requiere autenticación ni cookies de sesión.

    ### Flujo de Ejecución
    1. **Validación Sintáctica:**
        - Valida que el monto base sea un número decimal positivo dentro del rango permitido
          y con hasta dos cifras decimales.
    2. **Cálculo Financiero:**
        - Multiplica el valor base por la tasa de impuesto vigente (15%).
        - Cuantiza el impuesto resultante a dos decimales empleando redondeo hacia arriba en
          mitades.
    """

    value = service.calculate_tax_amount(amount=data.amount)

    return Response(
        success=True,
        pagination=False,
        message="Monto del impuesto calculado exitosamente.",
        data=ReadDecimalNumberDTO.model_construct(value=value),
    )
