from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.auth.dependencies import UserRepository, user_repository
from src.api.modules.inventory.repositories.category import CategoryRepository
from src.api.modules.inventory.repositories.product import ProductRepository
from src.api.modules.inventory.services.categories.create import CreateCategoryService
from src.api.modules.inventory.services.categories.delete import DeleteCategoryService
from src.api.modules.inventory.services.categories.get_list import GetListCategoryService
from src.api.modules.inventory.services.categories.update import UpdateCategoryService
from src.api.modules.inventory.services.products.add_product_wholesaler import (
    AddProductWholesaleService,
)
from src.api.modules.inventory.services.products.create import CreateProductPublicService
from src.api.modules.inventory.services.products.delete import DeleteProductService
from src.api.modules.inventory.services.products.get_list import GetListProductsService
from src.api.modules.inventory.services.products.get_products_wholesaler import (
    GetProductsWholesalerService,
)
from src.api.modules.inventory.services.products.update import UpdateProductService
from src.api.modules.users.dependencies import (
    CustomerWholesaleRepository,
    customer_wholesale_repository,
)
from src.api.settings.database import db_session


def category_repository(db: Annotated[AsyncSession, Depends(db_session)]) -> CategoryRepository:
    """Provee una instancia del repositorio de categorías."""

    return CategoryRepository(db=db)


def product_repository(db: Annotated[AsyncSession, Depends(db_session)]) -> ProductRepository:
    """Provee una instancia del repositorio de productos."""

    return ProductRepository(db=db)


def retrieve_list_products_service(
    product_repo: Annotated[ProductRepository, Depends(product_repository)],
) -> GetListProductsService:
    """Provee una instancia del servicio de consulta de una lista de productos."""

    return GetListProductsService(product_repo=product_repo)


def products_by_wholesaler_service(
    product_repo: Annotated[ProductRepository, Depends(product_repository)],
    user_repo: Annotated[UserRepository, Depends(user_repository)],
) -> GetProductsWholesalerService:
    """Provee una instancia del servicio de consulta de productos de un cliente mayorista."""

    return GetProductsWholesalerService(
        product_repo=product_repo,
        user_repo=user_repo,
    )


def create_product_public_service(
    product_repo: Annotated[ProductRepository, Depends(product_repository)],
    category_repo: Annotated[CategoryRepository, Depends(category_repository)],
) -> CreateProductPublicService:
    """Provee una instancia del servicio de creación de productos para el catálogo público."""

    return CreateProductPublicService(
        product_repo=product_repo,
        category_repo=category_repo,
    )


def add_product_wholesale_service(
    user_repo: Annotated[UserRepository, Depends(user_repository)],
    category_repo: Annotated[CategoryRepository, Depends(category_repository)],
    product_repo: Annotated[ProductRepository, Depends(product_repository)],
    customer_wholesale_repo: Annotated[
        CustomerWholesaleRepository, Depends(customer_wholesale_repository)
    ],
) -> AddProductWholesaleService:
    """Provee una instancia del servicio de creación de productos exclusivos para mayoristas."""

    return AddProductWholesaleService(
        customer_wholesale_repo=customer_wholesale_repo,
        category_repo=category_repo,
        product_repo=product_repo,
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
