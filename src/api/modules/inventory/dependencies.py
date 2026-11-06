from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.auth.dependencies import UserRepository, user_repository
from src.api.modules.inventory.repositories import (
    CategoryRepository,
    ProductRepository,
    WholesalerProductRepository,
)
from src.api.modules.inventory.services.categories import (
    CreateCategoryService,
    DeleteCategoryService,
    GetListCategoryService,
    UpdateCategoryService,
)
from src.api.modules.inventory.services.products import (
    CreateProductService,
    DeleteProductService,
    GetListProductService,
    GetProductService,
    UpdateProductService,
)
from src.api.modules.inventory.services.products.wholesaler import (
    AddProductWholesalerService,
    GetProductsWholesalerService,
)
from src.api.settings.database import db_session


def category_repository(db: Annotated[AsyncSession, Depends(db_session)]) -> CategoryRepository:
    """Provee una instancia del repositorio de categorías."""

    return CategoryRepository(db=db)


def product_repository(db: Annotated[AsyncSession, Depends(db_session)]) -> ProductRepository:
    """Provee una instancia del repositorio de productos."""

    return ProductRepository(db=db)


def wholesaler_product_repository(
    db: Annotated[AsyncSession, Depends(db_session)],
) -> WholesalerProductRepository:
    """Provee una instancia del repositorio de productos."""

    return WholesalerProductRepository(db=db)


def get_list_products_service(
    product_repo: Annotated[ProductRepository, Depends(product_repository)],
) -> GetListProductService:
    """Provee una instancia del servicio de consulta de una lista de productos."""

    return GetListProductService(product_repo=product_repo)


def get_product_service(
    product_repo: Annotated[ProductRepository, Depends(product_repository)],
) -> GetProductService:
    """Provee una instancia del servicio de consulta de un producto."""

    return GetProductService(product_repo=product_repo)


def get_products_wholesaler_service(
    user_repo: Annotated[UserRepository, Depends(user_repository)],
    wholesaler_product_repo: Annotated[
        WholesalerProductRepository, Depends(wholesaler_product_repository)
    ],
) -> GetProductsWholesalerService:
    """Provee una instancia del servicio de consulta de productos de un cliente mayorista."""

    return GetProductsWholesalerService(
        wholesaler_product_repo=wholesaler_product_repo,
        user_repo=user_repo,
    )


def create_product_service(
    product_repo: Annotated[ProductRepository, Depends(product_repository)],
    category_repo: Annotated[CategoryRepository, Depends(category_repository)],
) -> CreateProductService:
    """Provee una instancia del servicio de creación de productos para el catálogo público."""

    return CreateProductService(
        product_repo=product_repo,
        category_repo=category_repo,
    )


def add_product_wholesaler_service(
    user_repo: Annotated[UserRepository, Depends(user_repository)],
    category_repo: Annotated[CategoryRepository, Depends(category_repository)],
    wholesaler_product_repo: Annotated[
        WholesalerProductRepository, Depends(wholesaler_product_repository)
    ],
) -> AddProductWholesalerService:
    """Provee una instancia del servicio de creación de productos exclusivos para mayoristas."""

    return AddProductWholesalerService(
        category_repo=category_repo,
        wholesaler_product_repo=wholesaler_product_repo,
        user_repo=user_repo,
    )


def delete_product_service(
    product_repo: Annotated[ProductRepository, Depends(product_repository)],
) -> DeleteProductService:
    """Provee una instancia del servicio de eliminación de productos."""

    return DeleteProductService(product_repo=product_repo)


def update_product_service(
    product_repo: Annotated[ProductRepository, Depends(product_repository)],
    category_repo: Annotated[CategoryRepository, Depends(category_repository)],
) -> UpdateProductService:
    """Provee una instancia del servicio de actualización de productos."""

    return UpdateProductService(
        product_repo=product_repo,
        category_repo=category_repo,
    )


def create_category_service(
    category_repo: Annotated[CategoryRepository, Depends(category_repository)],
) -> CreateCategoryService:
    """Provee una instancia del servicio de creación de categorías."""

    return CreateCategoryService(category_repo=category_repo)


def delete_category_service(
    category_repo: Annotated[CategoryRepository, Depends(category_repository)],
) -> DeleteCategoryService:
    """Provee una instancia del servicio de eliminación de categorías."""

    return DeleteCategoryService(category_repo=category_repo)


def retrieve_list_category_service(
    category_repo: Annotated[CategoryRepository, Depends(category_repository)],
) -> GetListCategoryService:
    """Provee una instancia del servicio de consulta de una lista de categorías."""

    return GetListCategoryService(category_repo=category_repo)


def update_category_service(
    category_repo: Annotated[CategoryRepository, Depends(category_repository)],
) -> UpdateCategoryService:
    """Provee una instancia del servicio de actualización de categorías."""

    return UpdateCategoryService(category_repo=category_repo)
