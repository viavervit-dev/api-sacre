from typing import Any

from alembic.autogenerate import comparators, renderers
from alembic.autogenerate.api import AutogenContext
from alembic.operations import MigrateOperation, Operations
from alembic.operations.ops import UpgradeOps
from sqlalchemy import inspect


@Operations.register_operation(name="create_schema")
class CreateSchemaOp(MigrateOperation):
    """Operación de migración para crear un esquema."""

    def __init__(self, schema: str) -> None:
        self.schema = schema

    @classmethod
    def create_schema(cls, operations: Any, schema: str) -> Any:
        """Crea un esquema en la base de datos."""

        return operations.invoke(cls(schema=schema))

    def reverse(self) -> DropSchemaOp:
        """Devuelve la operación inversa para eliminar el esquema."""

        return DropSchemaOp(schema=self.schema)


@Operations.register_operation(name="drop_schema")
class DropSchemaOp(MigrateOperation):
    """Operación de migración para eliminar un esquema."""

    def __init__(self, schema: str) -> None:
        self.schema = schema

    @classmethod
    def drop_schema(cls, operations: Any, schema: str) -> Any:
        """Elimina un esquema de la base de datos."""

        return operations.invoke(cls(schema=schema))

    def reverse(self) -> CreateSchemaOp:
        """Devuelve la operación inversa para crear el esquema."""

        return CreateSchemaOp(schema=self.schema)


@Operations.register_operation(name="rename_schema")
class RenameSchemaOp(MigrateOperation):
    """Operación de migración para renombrar un esquema."""

    def __init__(self, old_schema: str, new_schema: str) -> None:
        self.old_schema = old_schema
        self.new_schema = new_schema

    @classmethod
    def rename_schema(cls, operations: Any, old_schema: str, new_schema: str) -> Any:
        """Renombra un esquema en la base de datos."""

        return operations.invoke(cls(old_schema=old_schema, new_schema=new_schema))

    def reverse(self) -> RenameSchemaOp:
        """Devuelve la operación inversa para restaurar el nombre previo del esquema."""

        return RenameSchemaOp(old_schema=self.new_schema, new_schema=self.old_schema)


# Renderers: dictan el código exacto que se escribe en el archivo de migración
@renderers.dispatch_for(target=CreateSchemaOp)
def render_create_schema(autogen_context: AutogenContext, op: CreateSchemaOp) -> str:
    """Renderiza la operación de creación de esquema en el archivo de migración."""

    return f"op.execute('CREATE SCHEMA IF NOT EXISTS \"{op.schema}\";')"


@renderers.dispatch_for(target=DropSchemaOp)
def render_drop_schema(autogen_context: AutogenContext, op: DropSchemaOp) -> str:
    """Renderiza la operación de eliminación de esquema en el archivo de migración."""

    return f"op.execute('DROP SCHEMA IF EXISTS \"{op.schema}\" RESTRICT;')"


@renderers.dispatch_for(target=RenameSchemaOp)
def render_rename_schema(autogen_context: AutogenContext, op: RenameSchemaOp) -> str:
    """Renderiza la operación de renombramiento de esquema en el archivo de migración."""

    return f'op.execute(\'ALTER SCHEMA "{op.old_schema}" RENAME TO "{op.new_schema}";\')'


# Comparador: compara SQLAlchemy Metadata
@comparators.dispatch_for(target="schema")
def compare_schemas(
    autogen_context: AutogenContext,
    upgrade_ops: UpgradeOps,
    schemas: set[str | None],
) -> None:
    """
    Compara los esquemas definidos en los modelos SQLAlchemy con los existentes en la base de
    datos. Detecta esquemas nuevos y detecta esquemas que se dejaron de usar y los elimina.
    """

    conn = autogen_context.connection

    if conn is None:
        return

    metadata = autogen_context.metadata

    # Obtener esquemas necesarios según los modelos (tablas y secuencias)
    table_schemas = {
        table.schema
        for table in metadata.tables.values()  # type: ignore[union-attr]
        if table.schema is not None
    }
    seq_schemas = {
        seq.schema
        for seq in metadata._sequences.values()  # type: ignore[union-attr]
        if seq.schema is not None
    }
    model_schemas = table_schemas | seq_schemas

    # Obtener esquemas existentes en la BD
    inspector = autogen_context.inspector or inspect(conn)
    existing_schemas = set(inspector.get_schema_names())

    # Detectar esquemas nuevos
    new_schemas: set[str] = set()

    for schema in model_schemas:
        if schema in ("public", "information_schema") or schema.startswith("pg_"):
            continue
        if not autogen_context.run_name_filters(schema, "schema", {}):
            continue
        if schema not in existing_schemas:
            new_schemas.add(schema)
        else:
            # Si el esquema existe pero aún no tiene tablas, esta migración lo inaugura
            db_tables = inspector.get_table_names(schema=schema)

            if len(db_tables) == 0:
                new_schemas.add(schema)

    for schema in sorted(new_schemas, reverse=True):
        upgrade_ops.ops.insert(0, CreateSchemaOp(schema=schema))

    # Detectar esquemas que ya no se usan
    candidate_drop_schemas = existing_schemas - model_schemas
    schemas_to_drop: set[str] = set()

    for schema in candidate_drop_schemas:
        if schema in ("public", "information_schema") or schema.startswith("pg_"):
            continue

        if not autogen_context.run_name_filters(schema, "schema", {}):
            continue

        # Verificar tablas del esquema en la base de datos
        db_tables = set(inspector.get_table_names(schema=schema))  # type: ignore[assignment]

        # Tablas de este esquema que ya se están eliminando en esta migración
        dropped_tables = {
            op.table_name  # type: ignore[attr-defined]
            for op in upgrade_ops.ops
            if op.__class__.__name__ == "DropTableOp" and getattr(op, "schema", None) == schema
        }
        remaining_tables = db_tables - dropped_tables  # type: ignore[operator]

        # Si aún quedan tablas que no se borran, no podemos eliminar el esquema
        if len(remaining_tables) > 0:
            continue

        # Verificar secuencias independientes del esquema
        db_sequences = set(inspector.get_sequence_names(schema=schema))
        dropped_sequences = {
            op.sequence_name  # type: ignore[attr-defined]
            for op in upgrade_ops.ops
            if op.__class__.__name__ == "DropSequenceOp" and getattr(op, "schema", None) == schema
        }
        remaining_sequences = db_sequences - dropped_sequences

        # Si no quedan ni tablas ni secuencias pendientes en el esquema, se elimina con seguridad
        if len(remaining_sequences) == 0:
            schemas_to_drop.add(schema)

    # Las eliminaciones de esquema
    for schema in sorted(schemas_to_drop):
        upgrade_ops.ops.append(DropSchemaOp(schema=schema))
