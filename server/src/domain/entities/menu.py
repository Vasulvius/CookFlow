from datetime import date
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import JSON
from sqlmodel import Column, Field, SQLModel


class MealType(str, Enum):
    """Enumeration for meal types."""

    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"


class Menu(SQLModel, table=True):
    """Menu entity with SQLModel."""

    __tablename__ = "menus"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str = Field()
    scheduled_at: date = Field(description="Menu date (day/month/year)")
    meal_type: MealType = Field(description="Type of meal")
    recipe_ids: List[str] = Field(default_factory=list, sa_column=Column(JSON))


class MenuCreate(SQLModel):
    """Model for creating a Menu."""

    name: str = Field(max_length=255)
    description: str = Field()
    scheduled_at: date = Field(description="Menu date (day/month/year)")
    meal_type: MealType = Field(description="Type of meal")
    recipe_ids: Optional[List[str]] = Field(default_factory=list)


class MenuRead(SQLModel):
    """Model for reading a Menu."""

    id: UUID
    name: str
    description: str
    scheduled_at: date
    meal_type: MealType
    recipe_ids: List[str]


class MenuUpdate(SQLModel):
    """Model for updating a Menu."""

    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None)
    scheduled_at: date | None = Field(default=None, description="Menu date (day/month/year)")
    meal_type: MealType | None = Field(default=None, description="Type of meal")
    recipe_ids: Optional[List[str]] = Field(default=None)
