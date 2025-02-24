from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.database import get_session
from src.entity.ingredient import Ingredient
from src.repository.ingredient_repository import IngredientRepository

router = APIRouter()


@router.post("/")
def create_ingredient(ingredient: Ingredient, session: Session = Depends(get_session)):
    repo = IngredientRepository(session)
    return repo.create(ingredient)


@router.get("/{ingredient_id}")
def get_ingredient(ingredient_id: int, session: Session = Depends(get_session)):
    repo = IngredientRepository(session)
    return repo.get_by_id(ingredient_id)


@router.get("/")
def get_all_ingredients(session: Session = Depends(get_session)):
    repo = IngredientRepository(session)
    return repo.get_all()
