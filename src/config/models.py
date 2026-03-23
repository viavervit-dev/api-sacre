# ruff: noqa: F401

"""
Registro central de modelos ORM.

Importa aquí TODOS los modelos SQLAlchemy del proyecto para que Alembic los detecte al generar
migraciones con autogenerate. Cada vez que crees un nuevo modelo, agrégalo a este archivo.
"""

from src.modules.customers.models.customer import CustomerModel
