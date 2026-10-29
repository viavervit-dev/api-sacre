"""crear secuencia shopping_order_number_seq

Revision ID: ce83944c4594
Revises: 50290f4f9030
Create Date: 2026-10-26 14:16:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ce83944c4594"
down_revision: str | Sequence[str] | None = "50290f4f9030"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE SEQUENCE IF NOT EXISTS orders.shopping_order_number_seq START WITH 1;")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP SEQUENCE IF EXISTS orders.shopping_order_number_seq;")

