from dataclasses import dataclass
from datetime import date
from enum import Enum
from uuid import UUID


class MealType(str, Enum):
    """Enumeration for meal types."""

    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"


@dataclass
class Menu:
    id: UUID
    name: str
    description: str
    scheduled_at: date
    meal_type: MealType
    recipe_ids: list[str]
