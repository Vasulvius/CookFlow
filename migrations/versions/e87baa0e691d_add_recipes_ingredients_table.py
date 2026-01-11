"""add recipes_ingredients table

Revision ID: e87baa0e691d
Revises: 4f85ae010be0
Create Date: 2026-01-11 21:53:10.379777

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e87baa0e691d"
down_revision: Union[str, Sequence[str], None] = "4f85ae010be0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE recipes_ingredients (
            recipe_id UUID REFERENCES recipes(id) ON DELETE CASCADE,
            ingredient_id UUID REFERENCES ingredients(id) ON DELETE CASCADE,
            quantity VARCHAR(100),
            unit VARCHAR(50),
            PRIMARY KEY (recipe_id, ingredient_id)
        );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS recipes_ingredients;")
