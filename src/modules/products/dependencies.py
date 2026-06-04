from typing import Annotated
from uuid import UUID

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions import ResourceNotFound
from src.config.database import get_db_session
from src.modules.products.models.product import Product
from src.modules.products.repositories.product import ProductRepository


async def get_product(
    product_id: Annotated[
        UUID,
        Path(
            title="ID del producto",
            description="El identificador único del producto en formato UUID v4.",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
    ],
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> Product:
    """
    Intercepta el ID del producto de la URL, busca el producto en la base de datos y lo retorna.
    Si el producto no existe, lanza un error 404.
    """

    exists = await ProductRepository.exists_product(filters={"id": product_id}, db=db)

    if not exists:
        raise ResourceNotFound()

    product = await ProductRepository.get_product_by_id(id=product_id, db=db)

    return product
