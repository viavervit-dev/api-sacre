# ruff: noqa: F401

"""
Registro central de modelos ORM.

Importa aquí TODOS los modelos SQLAlchemy del proyecto para que Alembic los detecte al generar
migraciones con autogenerate. Cada vez que crees un nuevo modelo, agrégalo a este archivo.
"""

# Modelos del módulo de administradores
from src.modules.admins.models.admin import Admin

# Modelos del módulo de autenticación
from src.modules.auth.models.jwt import JWTBlacklist
from src.modules.auth.models.permission import Group, Permission, PermissionGroup
from src.modules.auth.models.user import User, UserGroup

# Modelos del módulo de clientes
from src.modules.customers.models.customer import Customer

# Modelos del módulo de productos
from src.modules.products.models.category import Category
