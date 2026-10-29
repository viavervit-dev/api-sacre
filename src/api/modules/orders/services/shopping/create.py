from decimal import Decimal
from uuid import UUID

from fastapi.exceptions import RequestValidationError

from src.api.common.exceptions import ResourceNotFound
from src.api.common.utils import FinancialCalculationsMixin
from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.repositories.interfaces import IUserRepository
from src.api.modules.inventory.models.product import Product
from src.api.modules.inventory.repositories.interfaces import IProductRepository
from src.api.modules.orders.constants import (
    ShoppingOrderDescription,
    ShoppingOrderEntity,
    ShoppingOrderStatus,
)
from src.api.modules.orders.dto import (
    CreateOrderDTO,
    ReadCustomerDataDTO,
    ReadOrderDTO,
    ReadProductDataDTO,
)
from src.api.modules.orders.repositories.interfaces import IShoppingOrderRepository


class CreateOrderCustomerWholesaleService(FinancialCalculationsMixin):
    """Servicio encargado de la creación de órdenes de compra para clientes mayoristas."""

    def __init__(
        self,
        product_repo: IProductRepository,
        shopping_order_repo: IShoppingOrderRepository,
        user_repo: IUserRepository,
    ) -> None:
        self.__product_repo = product_repo
        self.__shopping_order_repo = shopping_order_repo
        self.__user_repo = user_repo
        self.__products: list[Product] = []

    async def create(self, data: CreateOrderDTO, customer_wholesale_id: UUID) -> ReadOrderDTO:
        """
        Crea una nueva orden de compra para un cliente mayorista.

        Raises:
            ResourceNotFound: Si el cliente mayorista no existe en la base de datos.
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        # Validar que el cliente mayorista exista
        user = await self.__user_repo.get_user(
            filters={
                "id": customer_wholesale_id,
                "role": UserRoles.CUSTOMER_WHOLESALE.value,
            },
            load_permissions=False,
        )

        if not user:
            raise ResourceNotFound()

        # Ejecutar validaciones de las reglas de negocio
        order_data = data.model_dump()
        await self.__run_business_validations(data=data)

        # Capturar la instantánea (snapshot) de los datos del cliente al momento de la orden
        order_data["customer_data"] = {
            "id": user.id,
            "name_or_company_name": user.customer_wholesale.name_or_company_name,
            "extra_contacts": user.customer_wholesale.extra_contacts,
            "location": user.customer_wholesale.location,
            "phone": user.customer_wholesale.phone,
            "ruc": user.customer_wholesale.ruc,
            "email": user.email,
        }

        # Enriquecer los ítems con información descriptiva actualizada desde el catálogo
        for product in order_data["product_data"]:
            for instance_product in self.__products:
                if instance_product.id == product["id"]:
                    product.update(
                        {
                            "name": instance_product.name,
                            "categories": instance_product.categories,
                            "description_short": instance_product.description_short,
                        }
                    )
                    break

        # Establecer el estado inicial de algunos campos
        order_data["order_number"] = await self.__shopping_order_repo.get_next_order_number()
        order_data["description"] = ShoppingOrderDescription.SHOPPING_ORDER.value
        order_data["status"] = ShoppingOrderStatus.PENDING_PAYMENT.value
        order_data["status_changed_at"] = None

        # Guardar información en la base de datos
        order = await self.__shopping_order_repo.create_order(data=order_data)

        # Extraer estructuras anidadas para instanciar el DTO de respuesta
        order_data = order.to_dict()
        customer_data = order_data.pop("customer_data")
        product_data = order_data.pop("product_data")

        return ReadOrderDTO.model_construct(
            **order_data,
            customer_data=ReadCustomerDataDTO.model_construct(**customer_data),
            product_data=[ReadProductDataDTO.model_construct(**p) for p in product_data],
        )

    async def __run_business_validations(self, data: CreateOrderDTO) -> None:
        """
        Ejecuta las validaciones de negocio previas a la creación de una orden.

        Raises:
            RequestValidationError: Si falla alguna validación de las reglas de negocio.
        """

        # Validar que el número de orden no haya sido registrado previamente
        exists = await self.__shopping_order_repo.exists_order(
            filters={"idempotency_key": data.idempotency_key},
        )

        if exists:
            raise RequestValidationError(
                errors=[
                    {
                        "loc": ("body", "idempotency_key"),
                        "msg": ShoppingOrderEntity.IDEMPOTENCY_KEY_EXISTS.value,
                        "type": "domain_validation",
                    }
                ]
            )

        # Inicializar acumuladores para verificar la consistencia financiera de los ítems
        calc_subtotal = Decimal("0.00")
        calc_tax = Decimal("0.00")
        calc_total = Decimal("0.00")
        calc_units = 0
        errors = []

        # Validar existencia de cada producto y cálculo de impuestos y totales por ítem
        for i, product in enumerate(data.product_data):
            instance = await self.__product_repo.get_product_by_id(id=product.id)

            if not instance:
                raise RequestValidationError(
                    errors=[
                        {
                            "loc": ("body", "product_data", i, "id"),
                            "msg": ShoppingOrderEntity.PRODUCT_NOT_FOUND.value,
                            "type": "domain_validation",
                        }
                    ]
                )

            # Guardar la instancia para enriquecer la orden sin volver a consultar la base de datos
            self.__products.append(instance)
            expected_tax = self.calculate_tax_amount(amount=product.subtotal)
            expected_total = product.subtotal + expected_tax

            if product.tax_amount != expected_tax:
                errors.append(
                    {
                        "loc": ("body", "product_data", i, "tax_amount"),
                        "msg": ShoppingOrderEntity.TAX_AMOUNT_PRODUCT_INVALID.value,
                        "type": "domain_validation",
                    }
                )
            if product.total != expected_total:
                errors.append(
                    {
                        "loc": ("body", "product_data", i, "total"),
                        "msg": ShoppingOrderEntity.TOTAL_PRODUCT_INVALID.value,
                        "type": "domain_validation",
                    }
                )

            calc_subtotal += product.subtotal
            calc_tax += product.tax_amount
            calc_total += product.total
            calc_units += product.units

        if errors:
            raise RequestValidationError(errors=errors)

        # Validar consistencia entre los totales de la cabecera y las sumatorias calculadas
        if data.subtotal != calc_subtotal:
            errors.append(
                {
                    "loc": ("body", "subtotal"),
                    "msg": ShoppingOrderEntity.SUBTOTAL_INVALID.value,
                    "type": "domain_validation",
                }
            )
        if data.tax_amount != calc_tax:
            errors.append(
                {
                    "loc": ("body", "tax_amount"),
                    "msg": ShoppingOrderEntity.TAX_AMOUNT_INVALID.value,
                    "type": "domain_validation",
                }
            )
        if data.units != calc_units:
            errors.append(
                {
                    "loc": ("body", "units"),
                    "msg": ShoppingOrderEntity.UNITS_INVALID.value,
                    "type": "domain_validation",
                }
            )
        if data.total != calc_total or data.total != (calc_subtotal + calc_tax):
            errors.append(
                {
                    "loc": ("body", "total"),
                    "msg": ShoppingOrderEntity.TOTAL_INVALID.value,
                    "type": "domain_validation",
                }
            )

        if errors:
            raise RequestValidationError(errors=errors)
