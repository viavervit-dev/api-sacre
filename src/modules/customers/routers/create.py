from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.response import Response
from src.common.schema import build_response_scheme_400, build_response_scheme_503
from src.config.database import get_db_session
from src.modules.auth.dto import ReadUserDTO
from src.modules.auth.repositories.user import UserRepository
from src.modules.customers.dto import CreateCustomerDTO, ReadCustomerDTO
from src.modules.customers.services.create import CreateCustomerService

router = APIRouter(prefix="/customer", tags=["Clientes"])


async def validations(
    data: CreateCustomerDTO,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> CreateCustomerDTO:
    """Ejecuta validaciones adicionales para la creación de un cliente."""

    all_errors: list[Any] = []

    # Lista de todas las validaciones que queremos correr
    checks = [
        data.check_email,
        data.check_phone,
        data.check_document_number,
    ]

    for check in checks:
        try:
            await check(session=session, user_repo=UserRepository)
        except RequestValidationError as e:
            all_errors.extend(e.errors())

    if all_errors:
        raise RequestValidationError(all_errors)

    return data


@router.post(
    path="/",
    response_description="Cliente creado exitosamente.",
    responses={
        400: build_response_scheme_400(dto_class=CreateCustomerDTO),
        503: build_response_scheme_503(db_unavailable=True),
    },
)
async def create_customer(
    data: Annotated[CreateCustomerDTO, Depends(validations)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> Response[ReadUserDTO[ReadCustomerDTO]]:
    """
    Endpoint para la creación de un cliente, recibe una petición con los datos necesarios y ejecuta
    validaciones adicionales. Si todo es correcto, crea el cliente en la base de datos, le asigna
    el rol correspondiente y devuelve su información.
    """

    service = CreateCustomerService(session=session, user_repo=UserRepository)
    customer = await service.create_customer(data=data)

    return Response(
        success=True,
        message="Cliente creado exitosamente.",
        data=customer,
    )
