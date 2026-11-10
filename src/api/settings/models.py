# ruff: noqa: F401

"""
Registro central de modelos ORM.

Importa aquí TODOS los modelos SQLAlchemy del proyecto para que Alembic los detecte al generar
migraciones con autogenerate. Cada vez que crees un nuevo modelo, agrégalo a este archivo.
"""

from src.api.modules.auth.models import Group, Permission, PermissionGroup, User, UserGroup
from src.api.modules.countries.models import Country
from src.api.modules.inventory.models import Category, Product, WholesalerProduct
from src.api.modules.orders.models import Order
from src.api.modules.users.models import Admin, Customer, Wholesaler
