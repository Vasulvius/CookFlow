from sqlmodel import Session, select
from src.entity.ingredient import Ingredient


class IngredientRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, ingredient: Ingredient):
        self.session.add(ingredient)
        self.session.commit()
        self.session.refresh(ingredient)
        return ingredient

    def get_by_id(self, ingredient_id: int):
        return self.session.exec(select(Ingredient).where(Ingredient.id == ingredient_id)).first()

    def get_all(self):
        return self.session.exec(select(Ingredient)).all()

    def delete(self, ingredient_id: int):
        ingredient = self.get_by_id(ingredient_id)
        if ingredient:
            self.session.delete(ingredient)
            self.session.commit()
