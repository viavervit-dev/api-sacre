from typing import Annotated

from fastapi import Depends

from src.api.modules.auth.dependencies import UserRepositoryDep
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
from src.api.modules.inventory.services.wholesaler_product import (
    AddProductWholesalerService,
    DeleteProductWholesalerService,
    GetListProductWholesalerService,
    GetProductsWholesalerService,
    UpdateProductWholesalerService,
)
from src.api.settings.database import DBSessionDep


def category_repository(db: DBSessionDep) -> CategoryRepository:
    """Provee una instancia del repositorio de categorías."""

    return CategoryRepository(db=db)


CategoryRepositoryDep = Annotated[CategoryRepository, Depends(category_repository)]


def product_repository(db: DBSessionDep) -> ProductRepository:
    """Provee una instancia del repositorio de productos."""

    return ProductRepository(db=db)


ProductRepositoryDep = Annotated[ProductRepository, Depends(product_repository)]


def wholesaler_product_repository(db: DBSessionDep) -> WholesalerProductRepository:
    """Provee una instancia del repositorio de productos."""

    return WholesalerProductRepository(db=db)


WholesalerProductRepositoryDep = Annotated[
    WholesalerProductRepository, Depends(wholesaler_product_repository)
]


def get_list_products_service(product_repo: ProductRepositoryDep) -> GetListProductService:
    """Provee una instancia del servicio de consulta de una lista de productos."""

    return GetListProductService(product_repo=product_repo)


GetListProductServiceDep = Annotated[GetListProductService, Depends(get_list_products_service)]


def get_product_service(product_repo: ProductRepositoryDep) -> GetProductService:
    """Provee una instancia del servicio de consulta de un producto."""

    return GetProductService(product_repo=product_repo)


GetProductServiceDep = Annotated[GetProductService, Depends(get_product_service)]


def get_products_wholesaler_service(
    wholesaler_product_repo: WholesalerProductRepositoryDep,
    user_repo: UserRepositoryDep,
) -> GetProductsWholesalerService:
    """Provee una instancia del servicio de consulta de productos de un cliente mayorista."""

    return GetProductsWholesalerService(
        wholesaler_product_repo=wholesaler_product_repo,
        user_repo=user_repo,
    )


GetProductsWholesalerServiceDep = Annotated[
    GetProductsWholesalerService, Depends(get_products_wholesaler_service)
]


def get_list_products_wholesaler_service(
    wholesaler_product_repo: WholesalerProductRepositoryDep,
) -> GetListProductWholesalerService:
    """Provee una instancia del servicio de consulta de productos de clientes mayoristas."""

    return GetListProductWholesalerService(wholesaler_product_repo=wholesaler_product_repo)


GetListProductWholesalerServiceDep = Annotated[
    GetListProductWholesalerService, Depends(get_list_products_wholesaler_service)
]


def create_product_service(
    product_repo: ProductRepositoryDep,
    category_repo: CategoryRepositoryDep,
) -> CreateProductService:
    """Provee una instancia del servicio de creación de productos para el catálogo público."""

    return CreateProductService(
        product_repo=product_repo,
        category_repo=category_repo,
    )


CreateProductServiceDep = Annotated[CreateProductService, Depends(create_product_service)]


def add_product_wholesaler_service(
    user_repo: UserRepositoryDep,
    category_repo: CategoryRepositoryDep,
    wholesaler_product_repo: WholesalerProductRepositoryDep,
) -> AddProductWholesalerService:
    """Provee una instancia del servicio de creación de productos para clientes mayoristas."""

    return AddProductWholesalerService(
        category_repo=category_repo,
        wholesaler_product_repo=wholesaler_product_repo,
        user_repo=user_repo,
    )


AddProductWholesalerServiceDep = Annotated[
    AddProductWholesalerService, Depends(add_product_wholesaler_service)
]


def update_product_wholesaler_service(
    category_repo: CategoryRepositoryDep,
    wholesaler_product_repo: WholesalerProductRepositoryDep,
) -> UpdateProductWholesalerService:
    """Provee una instancia del servicio de actualización de productos de clientes mayoristas."""

    return UpdateProductWholesalerService(
        category_repo=category_repo,
        wholesaler_product_repo=wholesaler_product_repo,
    )


UpdateProductWholesalerServiceDep = Annotated[
    UpdateProductWholesalerService, Depends(update_product_wholesaler_service)
]


def delete_product_wholesaler_service(
    wholesaler_product_repo: WholesalerProductRepositoryDep,
) -> DeleteProductWholesalerService:
    """Provee una instancia del servicio de eliminación de productos de clientes mayoristas."""

    return DeleteProductWholesalerService(wholesaler_product_repo=wholesaler_product_repo)


DeleteProductWholesalerServiceDep = Annotated[
    DeleteProductWholesalerService, Depends(delete_product_wholesaler_service)
]


def delete_product_service(product_repo: ProductRepositoryDep) -> DeleteProductService:
    """Provee una instancia del servicio de eliminación de productos."""

    return DeleteProductService(product_repo=product_repo)


DeleteProductServiceDep = Annotated[DeleteProductService, Depends(delete_product_service)]


def update_product_service(
    product_repo: ProductRepositoryDep,
    category_repo: CategoryRepositoryDep,
) -> UpdateProductService:
    """Provee una instancia del servicio de actualización de productos."""

    return UpdateProductService(
        product_repo=product_repo,
        category_repo=category_repo,
    )


UpdateProductServiceDep = Annotated[UpdateProductService, Depends(update_product_service)]


def create_category_service(category_repo: CategoryRepositoryDep) -> CreateCategoryService:
    """Provee una instancia del servicio de creación de categorías."""

    return CreateCategoryService(category_repo=category_repo)


CreateCategoryServiceDep = Annotated[CreateCategoryService, Depends(create_category_service)]


def delete_category_service(category_repo: CategoryRepositoryDep) -> DeleteCategoryService:
    """Provee una instancia del servicio de eliminación de categorías."""

    return DeleteCategoryService(category_repo=category_repo)


DeleteCategoryServiceDep = Annotated[DeleteCategoryService, Depends(delete_category_service)]


def get_list_category_service(category_repo: CategoryRepositoryDep) -> GetListCategoryService:
    """Provee una instancia del servicio de consulta de una lista de categorías."""

    return GetListCategoryService(category_repo=category_repo)


GetListCategoryServiceDep = Annotated[GetListCategoryService, Depends(get_list_category_service)]


def update_category_service(category_repo: CategoryRepositoryDep) -> UpdateCategoryService:
    """Provee una instancia del servicio de actualización de categorías."""

    return UpdateCategoryService(category_repo=category_repo)


UpdateCategoryServiceDep = Annotated[UpdateCategoryService, Depends(update_category_service)]
