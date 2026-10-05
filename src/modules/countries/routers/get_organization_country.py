from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from src.common.response import Response
from src.common.schema import response_scheme_404, response_scheme_503
from src.modules.countries.dependencies import get_retrieve_organization_country_service
from src.modules.countries.dto import ReadAdministrativeStructureDTO
from src.modules.countries.services.get_organization_country import (
    RetrieveOrganizationCountryService,
)

organization_country_router = APIRouter(prefix="/countries", tags=["Países"])


@organization_country_router.get(
    path="/{country}/",
    response_description="**(OK)** Organización territorial del país obtenida exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: response_scheme_404(),
        status.HTTP_503_SERVICE_UNAVAILABLE: response_scheme_503(db_unavailable=True),
    },
)
async def get_organization_country(
    country: Annotated[
        str,
        Path(
            title="Nombre del país.",
            description="Nombre oficial del país cuya organización territorial se consulta.",
        ),
    ],
    service: Annotated[
        RetrieveOrganizationCountryService,
        Depends(get_retrieve_organization_country_service),
    ],
) -> Response[ReadAdministrativeStructureDTO]:
    """
    Permite consultar la organización territorial jerárquica de un país registrado en el
    sistema. Proporciona a las aplicaciones cliente los datos básicos necesarios para poblar
    selectores geográficos de registro, facturación y direcciones de entrega sin cargar
    estructuras territoriales pesadas.

    ### Requisitos de Acceso
    - **Acceso Público:** Endpoint abierto. No requiere autenticación ni cookies de sesión.

    ### Flujo de Ejecución
    1. **Validación del Parámetro de Ruta (`country`):**
        - Extrae el nombre del país desde la URL y valida su tipo sintáctico (`str`).
    2. **Consulta en Base de Datos:**
        - Busca el país en la tabla `countries.country` filtrando por el campo `name`
         cargando únicamente la columna `administrative_structure`.
    3. **Manejo de Recurso No Encontrado:**
        - Si el país solicitado no existe en la base de datos, levanta código HTTP 404 Not Found.
    4. **Serialización Dinámica:**
        - Mapea la estructura jerárquica al DTO de lectura.
    """

    organization_country = await service.get_organization_country(country=country)

    return Response(
        success=True,
        pagination=False,
        message="Organización territorial del país obtenida exitosamente.",
        data=organization_country,
    )
