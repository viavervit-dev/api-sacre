from typing import Annotated, Any

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.response import Response
from src.common.schema import build_response_scheme_400, build_response_scheme_503
from src.config.database import get_db_session
from src.modules.products.dto import CreateProductDTO, ReadProductDTO
from src.modules.products.repositories.product import ProductRepository
from src.modules.products.services.create_product import CreateProductService

router = APIRouter(prefix="/product", tags=["Productos"])


async def validations(
    data: CreateProductDTO,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> CreateProductDTO:
    """Ejecuta validaciones adicionales para la creación de un producto."""

    all_errors: list[Any] = []

    # Lista de todas las validaciones que queremos correr
    checks = [data.check_name, data.check_images_urls, data.check_categories]

    for check in checks:
        try:
            await check(session=session, product_repo=ProductRepository)
        except RequestValidationError as e:
            all_errors.extend(e.errors())

    if all_errors:
        raise RequestValidationError(all_errors)

    return data


@router.post(
    path="/",
    response_description="Producto creado exitosamente.",
    status_code=status.HTTP_201_CREATED,
    responses={
        400: build_response_scheme_400(dto_class=CreateProductDTO),
        503: build_response_scheme_503(db_unavailable=True),
    },
)
async def create_product(
    data: Annotated[CreateProductDTO, Depends(validations)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> Response[ReadProductDTO]:
    """
    Endpoint para la creación de un producto, recibe una petición con los datos necesarios y
    ejecuta validaciones adicionales. Si todo es correcto, crea el producto en la base de datos
    y devuelve su información.
    """

    service = CreateProductService(session=session, product_repo=ProductRepository)
    product = await service.create_product(data=data)

    return Response(
        success=True,
        message="Producto creado exitosamente.",
        data=product,
    )
