# ruff: noqa: F401

"""
Registro central de modelos ORM.

Importa aquí TODOS los modelos SQLAlchemy del proyecto para que Alembic los detecte al generar
migraciones con autogenerate. Cada vez que crees un nuevo modelo, agrégalo a este archivo.
"""

# Modelos del módulo de autenticación
from src.modules.auth.models.permission import Group, Permission, PermissionGroup
from src.modules.auth.models.user import User, UserGroup

# Modelos del módulo de países
from src.modules.countries.models.country import Country

# Modelos del módulo de productos
from src.modules.inventory.models.category import Category
from src.modules.inventory.models.product import Product

# Modelos del módulo de usuarios
from src.modules.users.models.admin import Admin
from src.modules.users.models.customer import Customer
from src.modules.users.models.wholesale import CustomerWholesale
