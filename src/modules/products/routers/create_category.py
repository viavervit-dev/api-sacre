from typing import Annotated, Any

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.response import Response
from src.common.schema import build_response_scheme_400, build_response_scheme_503
from src.config.database import get_db_session
from src.modules.products.dto import CreateCategoryDTO, ReadCategoryDTO
from src.modules.products.repositories.product import ProductRepository
from src.modules.products.services.create_category import CreateCategoryService

router = APIRouter(prefix="/product", tags=["Productos"])


async def validations(
    data: CreateCategoryDTO,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> CreateCategoryDTO:
    """Ejecuta validaciones adicionales para la creación de una categoría."""

    all_errors: list[Any] = []

    # Lista de todas las validaciones que queremos correr
    checks = [data.check_name]

    for check in checks:
        try:
            await check(db=db, product_repo=ProductRepository)
        except RequestValidationError as e:
            all_errors.extend(e.errors())

    if all_errors:
        raise RequestValidationError(all_errors)

    return data


@router.post(
    path="/category/",
    response_description="Categoría creada exitosamente.",
    status_code=status.HTTP_201_CREATED,
    responses={
        400: build_response_scheme_400(dto_class=CreateCategoryDTO),
        503: build_response_scheme_503(db_unavailable=True),
    },
)
async def create_category(
    data: Annotated[CreateCategoryDTO, Depends(validations)],
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> Response[ReadCategoryDTO]:
    """
    Endpoint para la creación de una categoría de productos, recibe una petición con los datos
    necesarios y ejecuta validaciones adicionales. Si todo es correcto, crea la categoría en la
    base de datos y devuelve su información.
    """

    service = CreateCategoryService(db=db, product_repo=ProductRepository)
    category = await service.create_category(data=data)

    return Response(
        success=True,
        message="Categoría creada exitosamente.",
        data=category,
    )
