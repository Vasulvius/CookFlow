class IngredientRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def add_ingredient(self, name: str, category: str) -> None:
        query = "INSERT INTO ingredients (name, category) VALUES (?, ?);"
        self.db_session.execute(query, (name, category))
        self.db_session.commit()

    def get_ingredient_by_id(self, ingredient_id: int) -> dict:
        query = "SELECT * FROM ingredients WHERE id = ?;"
        result = self.db_session.execute(query, (ingredient_id,)).fetchone()
        if result:
            return dict(result)
        return {}

    def list_ingredients(self) -> list:
        query = "SELECT * FROM ingredients;"
        results = self.db_session.execute(query).fetchall()
        return [dict(row) for row in results]
