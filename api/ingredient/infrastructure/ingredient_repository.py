from typing import List, Optional
from uuid import UUID

from api.infrastructure.database.abstract_repository import AbstractRepository
from api.ingredient.domain.ingredient import Ingredient


class IngredientRepository(AbstractRepository):
    """Repository for ingredient data access."""

    def create(self, name: str, category: Optional[str] = None) -> Ingredient:
        """Create a new ingredient."""
        with self.get_connection() as conn:
            with self.get_cursor(conn) as cursor:
                cursor.execute(
                    """
                    INSERT INTO ingredients (name, category)
                    VALUES (%s, %s)
                    RETURNING id, name, category, created_at, updated_at;
                    """,
                    (name, category),
                )
                result = cursor.fetchone()
                return Ingredient.from_dict(dict(result))

    def get_by_id(self, ingredient_id: UUID) -> Optional[Ingredient]:
        """Get an ingredient by ID."""
        with self.get_connection() as conn:
            with self.get_cursor(conn) as cursor:
                cursor.execute(
                    """
                    SELECT id, name, category, created_at, updated_at
                    FROM ingredients
                    WHERE id = %s;
                    """,
                    (str(ingredient_id),),
                )
                result = cursor.fetchone()
                if result:
                    return Ingredient.from_dict(dict(result))
                return None

    def list_all(self) -> List[Ingredient]:
        """List all ingredients."""
        with self.get_connection() as conn:
            with self.get_cursor(conn) as cursor:
                cursor.execute(
                    """
                    SELECT id, name, category, created_at, updated_at
                    FROM ingredients
                    ORDER BY created_at DESC;
                    """
                )
                results = cursor.fetchall()
                return [Ingredient.from_dict(dict(row)) for row in results]

    def update(
        self, ingredient_id: UUID, name: Optional[str] = None, category: Optional[str] = None
    ) -> Optional[Ingredient]:
        """Update an ingredient."""
        with self.get_connection() as conn:
            with self.get_cursor(conn) as cursor:
                # Build dynamic update query
                updates = []
                params = []

                if name is not None:
                    updates.append("name = %s")
                    params.append(name)
                if category is not None:
                    updates.append("category = %s")
                    params.append(category)

                if not updates:
                    return self.get_by_id(ingredient_id)

                updates.append("updated_at = CURRENT_TIMESTAMP")
                params.append(str(ingredient_id))

                query = f"""
                    UPDATE ingredients
                    SET {", ".join(updates)}
                    WHERE id = %s
                    RETURNING id, name, category, created_at, updated_at;
                """

                cursor.execute(query, params)
                result = cursor.fetchone()
                if result:
                    return Ingredient.from_dict(dict(result))
                return None

    def delete(self, ingredient_id: UUID) -> bool:
        """Delete an ingredient."""
        with self.get_connection() as conn:
            with self.get_cursor(conn) as cursor:
                cursor.execute(
                    """
                    DELETE FROM ingredients
                    WHERE id = %s;
                    """,
                    (str(ingredient_id),),
                )
                return cursor.rowcount > 0
