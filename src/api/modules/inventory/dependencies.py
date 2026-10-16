from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.auth.dependencies import get_user_repository
from src.api.modules.auth.repositories.user import UserRepository
from src.api.modules.inventory.repositories.category import CategoryRepository
from src.api.modules.inventory.repositories.product import ProductRepository
from src.api.modules.inventory.services.categories.create_category import CreateCategoryService
from src.api.modules.inventory.services.categories.delete_category import DeleteCategoryService
from src.api.modules.inventory.services.categories.get_list_category import (
    RetrieveListCategoryService,
)
from src.api.modules.inventory.services.categories.update_category import UpdateCategoryService
from src.api.modules.inventory.services.products.add_product_wholesaler import (
    AddProductWholesaleService,
)
from src.api.modules.inventory.services.products.create_product import CreateProductPublicService
from src.api.modules.inventory.services.products.delete_product import DeleteProductService
from src.api.modules.inventory.services.products.get_list_products import (
    RetrieveListProductsService,
)
from src.api.modules.inventory.services.products.get_products_wholesaler import (
    RetrieveProductsWholesalerService,
)
from src.api.modules.inventory.services.products.update_product import UpdateProductService
from src.api.modules.users.dependencies import customer_wholesale_repository
from src.api.modules.users.repositories.customer_wholesale import CustomerWholesaleRepository
from src.api.settings.database import get_db_session


def category_repository(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> CategoryRepository:
    """Provee una instancia del repositorio de categorías."""

    return CategoryRepository(db=db)


def product_repository(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> ProductRepository:
    """Provee una instancia del repositorio de productos."""

    return ProductRepository(db=db)


def retrieve_list_products_service(
    product_repo: Annotated[ProductRepository, Depends(product_repository)],
) -> RetrieveListProductsService:
    """Provee una instancia del servicio de consulta de una lista de productos."""

    return RetrieveListProductsService(product_repo=product_repo)


def products_by_wholesaler_service(
    product_repo: Annotated[ProductRepository, Depends(product_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> RetrieveProductsWholesalerService:
    """Provee una instancia del servicio de consulta de productos de un cliente mayorista."""

    return RetrieveProductsWholesalerService(
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
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
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
) -> RetrieveListCategoryService:
    """Provee una instancia del servicio de consulta de una lista de categorías."""

    return RetrieveListCategoryService(category_repo=category_repo)


def update_category_service(
    category_repo: Annotated[CategoryRepository, Depends(category_repository)],
) -> UpdateCategoryService:
    """Provee una instancia del servicio de actualización de categorías."""

    return UpdateCategoryService(category_repo=category_repo)
