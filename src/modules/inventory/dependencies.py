from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db_session
from src.modules.inventory.repositories.category import CategoryRepository
from src.modules.inventory.repositories.product import ProductRepository
from src.modules.inventory.services.categories.create_category import CreateCategoryService
from src.modules.inventory.services.categories.delete_category import DeleteCategoryService
from src.modules.inventory.services.categories.get_category import RetrieveCategoryService
from src.modules.inventory.services.categories.update_category import UpdateCategoryService
from src.modules.inventory.services.products.add_product_wholesaler import (
    AddProductWholesaleService,
)
from src.modules.inventory.services.products.create_product import CreateProductService
from src.modules.inventory.services.products.delete_product import DeleteProductService
from src.modules.inventory.services.products.get_list_products import RetrieveListProductsService
from src.modules.inventory.services.products.get_products_wholesaler import (
    RetrieveProductsWholesalerService,
)
from src.modules.inventory.services.products.update_product import UpdateProductService
from src.modules.users.dependencies import get_customer_wholesale_repository
from src.modules.users.repositories.wholesale import CustomerWholesaleRepository


def get_category_repository(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> CategoryRepository:
    """Provee una instancia del repositorio de categorías."""

    return CategoryRepository(db=db)


def get_product_repository(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> ProductRepository:
    """Provee una instancia del repositorio de productos."""

    return ProductRepository(db=db)


def get_retrieve_list_products_service(
    product_repo: Annotated[ProductRepository, Depends(get_product_repository)],
) -> RetrieveListProductsService:
    """Provee una instancia del servicio de consulta de productos."""

    return RetrieveListProductsService(product_repo=product_repo)


def get_products_by_wholesaler_service(
    product_repo: Annotated[ProductRepository, Depends(get_product_repository)],
) -> RetrieveProductsWholesalerService:
    """Provee una instancia del servicio de consulta de productos de un cliente mayorista."""

    return RetrieveProductsWholesalerService(product_repo=product_repo)


def get_create_product_service(
    product_repo: Annotated[ProductRepository, Depends(get_product_repository)],
    category_repo: Annotated[CategoryRepository, Depends(get_category_repository)],
) -> CreateProductService:
    """Provee una instancia del servicio de creación de productos."""

    return CreateProductService(
        product_repo=product_repo,
        category_repo=category_repo,
    )


def get_add_product_wholesale_service(
    category_repo: Annotated[CategoryRepository, Depends(get_category_repository)],
    product_repo: Annotated[ProductRepository, Depends(get_product_repository)],
    customer_wholesale_repo: Annotated[
        CustomerWholesaleRepository, Depends(get_customer_wholesale_repository)
    ],
) -> AddProductWholesaleService:
    """Provee una instancia del servicio de creación de productos exclusivos para mayoristas."""

    return AddProductWholesaleService(
        customer_wholesale_repo=customer_wholesale_repo,
        category_repo=category_repo,
        product_repo=product_repo,
    )


def get_delete_product_service(
    product_repo: Annotated[ProductRepository, Depends(get_product_repository)],
) -> DeleteProductService:
    """Provee una instancia del servicio de eliminación de productos."""

    return DeleteProductService(product_repo=product_repo)


def get_update_product_service(
    product_repo: Annotated[ProductRepository, Depends(get_product_repository)],
    category_repo: Annotated[CategoryRepository, Depends(get_category_repository)],
) -> UpdateProductService:
    """Provee una instancia del servicio de actualización de productos."""

    return UpdateProductService(
        product_repo=product_repo,
        category_repo=category_repo,
    )


def get_create_category_service(
    category_repo: Annotated[CategoryRepository, Depends(get_category_repository)],
) -> CreateCategoryService:
    """Provee una instancia del servicio de creación de categorías."""

    return CreateCategoryService(category_repo=category_repo)


def get_delete_category_service(
    category_repo: Annotated[CategoryRepository, Depends(get_category_repository)],
) -> DeleteCategoryService:
    """Provee una instancia del servicio de eliminación de categorías."""

    return DeleteCategoryService(category_repo=category_repo)


def get_retrieve_category_service(
    category_repo: Annotated[CategoryRepository, Depends(get_category_repository)],
) -> RetrieveCategoryService:
    """Provee una instancia del servicio de consulta de categorías."""

    return RetrieveCategoryService(category_repo=category_repo)


def get_update_category_service(
    category_repo: Annotated[CategoryRepository, Depends(get_category_repository)],
) -> UpdateCategoryService:
    """Provee una instancia del servicio de actualización de categorías."""

    return UpdateCategoryService(category_repo=category_repo)
