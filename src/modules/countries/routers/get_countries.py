from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.common.response import Response
from src.common.schema import response_scheme_503
from src.modules.countries.dependencies import get_retrieve_contries_service
from src.modules.countries.dto import ReadCountryDTO
from src.modules.countries.services.get_countries import RetrieveContriesService

countries_router = APIRouter(prefix="/countries", tags=["Países"])


@countries_router.get(
    path="/",
    response_description="**(OK)** Lista de países obtenida exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: response_scheme_503(db_unavailable=True),
    },
)
async def get_countries(
    service: Annotated[RetrieveContriesService, Depends(get_retrieve_contries_service)],
) -> Response[list[ReadCountryDTO]]:
    """
    Obtiene la lista de países disponibles en el sistema.

    ### Descripción
    Consulta y retorna el catálogo general de países registrados con su nombre oficial y código
    internacional (ISO). Proporciona a las aplicaciones cliente los datos básicos necesarios
    para poblar selectores geográficos de registro, facturación y direcciones de entrega sin
    cargar estructuras territoriales pesadas.

    ### Requisitos de Acceso
    - **Acceso Público:** Endpoint abierto. No requiere autenticación ni cookies de sesión.

    ### Flujo de Ejecución
    1. **Consulta en Base de Datos:**
        - Realiza una consulta sobre la tabla `countries.country` ordenando los registros
         alfabéticamente por el nombre del país.
    2. **Serialización Dinámica:**
        - Mapea la lista de países al DTO de lectura.
    """

    countries = await service.get_countries()

    return Response(
        success=True,
        pagination=False,
        message="Lista de países obtenida exitosamente.",
        data=countries,
    )
