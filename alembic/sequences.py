from typing import Any

from alembic.autogenerate import comparators, renderers
from alembic.autogenerate.api import AutogenContext
from alembic.operations import MigrateOperation, Operations
from alembic.operations.ops import UpgradeOps
from sqlalchemy import text


@Operations.register_operation(name="create_sequence")
class CreateSequenceOp(MigrateOperation):
    """Operación de migración para crear una secuencia."""

    def __init__(self, sequence_name: str, schema: str | None = None, start: int = 1) -> None:
        self.sequence_name = sequence_name
        self.schema = schema
        self.start = start

    @classmethod
    def create_sequence(
        cls,
        operations: Any,
        sequence_name: str,
        schema: str | None = None,
        start: int = 1,
    ) -> Any:
        """Crea una secuencia en la base de datos."""

        return operations.invoke(cls(sequence_name, schema=schema, start=start))

    def reverse(self) -> DropSequenceOp:
        """Devuelve la operación inversa para eliminar la secuencia."""

        return DropSequenceOp(self.sequence_name, schema=self.schema)


@Operations.register_operation(name="drop_sequence")
class DropSequenceOp(MigrateOperation):
    """Operación de migración para eliminar una secuencia."""

    def __init__(self, sequence_name: str, schema: str | None = None) -> None:
        self.sequence_name = sequence_name
        self.schema = schema

    @classmethod
    def drop_sequence(cls, operations: Any, sequence_name: str, schema: str | None = None) -> Any:
        """Elimina una secuencia de la base de datos."""

        return operations.invoke(cls(sequence_name, schema=schema))

    def reverse(self) -> CreateSequenceOp:
        """Devuelve la operación inversa para crear la secuencia."""

        return CreateSequenceOp(self.sequence_name, schema=self.schema)


# Renderers: dictan el código exacto que se escribe en el archivo de migración
@renderers.dispatch_for(target=CreateSequenceOp)
def render_create_sequence(autogen_context: AutogenContext, op: CreateSequenceOp) -> str:
    """Renderiza la operación de creación de secuencia en el archivo de migración."""

    full_name = f'"{op.schema}"."{op.sequence_name}"' if op.schema else f'"{op.sequence_name}"'
    start_clause = f" START WITH {op.start}" if op.start is not None else ""

    return f"op.execute('CREATE SEQUENCE IF NOT EXISTS {full_name}{start_clause};')"


@renderers.dispatch_for(target=DropSequenceOp)
def render_drop_sequence(autogen_context: AutogenContext, op: DropSequenceOp) -> str:
    """Renderiza la operación de eliminación de secuencia en el archivo de migración."""

    full_name = f'"{op.schema}"."{op.sequence_name}"' if op.schema else f'"{op.sequence_name}"'

    return f"op.execute('DROP SEQUENCE IF EXISTS {full_name};')"


# Comparador: compara SQLAlchemy Metadata vs PostgreSQL
@comparators.dispatch_for(target="schema")
def compare_sequences(
    autogen_context: AutogenContext,
    upgrade_ops: UpgradeOps,
    schemas: set[str | None],
) -> None:
    """
    Compara las secuencias definidas en SQLAlchemy Metadata con las existentes en la base de datos.
    Agrega operaciones de creación o eliminación de secuencias según sea necesario.
    """

    conn = autogen_context.connection

    if conn is None:
        return

    # Secuencias definidas en los modelos (metadata)
    metadata_sequences: dict[tuple[str | None, str], Any] = {}

    for seq in autogen_context.metadata._sequences.values():  # type: ignore[union-attr]
        # Validar filtros de nombres de Alembic (include_name)
        if seq.schema and not autogen_context.run_name_filters(seq.schema, "schema", {}):
            continue
        if not autogen_context.run_name_filters(seq.name, "sequence", {"schema_name": seq.schema}):  # type: ignore[arg-type]
            continue

        metadata_sequences[(seq.schema, seq.name)] = seq

    # Secuencias existentes (excluyendo las que pertenecen a columnas SERIAL o IDENTITY)
    query = text("""
        SELECT n.nspname AS schema_name, c.relname AS sequence_name
        FROM pg_catalog.pg_class c
        JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relkind = 'S'
          AND NOT EXISTS (
              SELECT 1 FROM pg_catalog.pg_depend d
              WHERE d.objid = c.oid
                AND d.deptype IN ('a', 'i')
          );
    """)
    result = conn.execute(query).fetchall()
    db_sequences = {
        (row[0], row[1])
        for row in result
        if (
            row[0] not in ("public", "information_schema")
            and not (row[0] and row[0].startswith("pg_"))
            and autogen_context.run_name_filters(row[0], "schema", {})
        )
        or (row[0] in (None, "public") and None in schemas)
    }

    # Detectar secuencias nuevas (se insertan DESPUÉS de cualquier CreateSchemaOp)
    for (schema, name), seq in metadata_sequences.items():
        if (schema, name) not in db_sequences:
            start_val = seq.start if seq.start is not None else 1
            insert_idx = 0

            for idx, op in enumerate(upgrade_ops.ops):
                if op.__class__.__name__ == "CreateSchemaOp":
                    insert_idx = idx + 1

            upgrade_ops.ops.insert(
                insert_idx, CreateSequenceOp(name, schema=schema, start=start_val)
            )

    # Detectar secuencias eliminadas en los modelos (se insertan ANTES de DropSchemaOp)
    for schema, name in db_sequences:
        if (schema, name) not in metadata_sequences:
            insert_drop_idx = len(upgrade_ops.ops)
            for idx, op in enumerate(upgrade_ops.ops):
                if op.__class__.__name__ == "DropSchemaOp":
                    insert_drop_idx = idx
                    break

            upgrade_ops.ops.insert(insert_drop_idx, DropSequenceOp(name, schema=schema))
