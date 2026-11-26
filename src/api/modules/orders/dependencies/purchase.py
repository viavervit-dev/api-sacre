from typing import Annotated

from fastapi import Depends

from src.api.common.payment.dependencies import CreatePaymentLinkServiceDep
from src.api.modules.auth.dependencies import UserRepositoryDep
from src.api.modules.inventory.dependencies import (
    ProductRepositoryDep,
    WholesalerProductRepositoryDep,
)
from src.api.modules.orders.repositories import OrderRepositoryDep
from src.api.modules.orders.services.purchase import (
    CreateOrderWholesalerService,
    GetListOrderService,
    GetOrderService,
)


def get_list_order_service(order_repo: OrderRepositoryDep) -> GetListOrderService:
    """
    Dependencia que provee el servicio encargado de listar órdenes de compra de forma paginada.
    """

    return GetListOrderService(order_repo=order_repo)


GetListOrderServiceDep = Annotated[GetListOrderService, Depends(get_list_order_service)]


def get_order_service(order_repo: OrderRepositoryDep) -> GetOrderService:
    """
    Dependencia que provee el servicio encargado de consultar el detalle de una orden de compra.
    """

    return GetOrderService(order_repo=order_repo)


GetOrderServiceDep = Annotated[GetOrderService, Depends(get_order_service)]


def create_order_wholesaler_service(
    create_payment_link_service: CreatePaymentLinkServiceDep,
    order_repo: OrderRepositoryDep,
    user_repo: UserRepositoryDep,
    product_repo: ProductRepositoryDep,
    wholesaler_product_repo: WholesalerProductRepositoryDep,
) -> CreateOrderWholesalerService:
    """
    Dependencia que provee el servicio encargado de registrar órdenes de compra para
    clientes mayoristas.
    """

    return CreateOrderWholesalerService(
        create_payment_link_service=create_payment_link_service,
        wholesaler_product_repo=wholesaler_product_repo,
        product_repo=product_repo,
        order_repo=order_repo,
        user_repo=user_repo,
    )


CreateOrderWholesalerServiceDep = Annotated[
    CreateOrderWholesalerService, Depends(create_order_wholesaler_service)
]
