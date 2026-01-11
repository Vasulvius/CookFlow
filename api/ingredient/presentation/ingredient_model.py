from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class IngredientCreate(BaseModel):
    """Model for creating a new ingredient."""

    name: str = Field(..., min_length=1, max_length=255)
    category: Optional[str] = Field(None, max_length=255)


class IngredientUpdate(BaseModel):
    """Model for updating an ingredient."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, max_length=255)


class IngredientResponse(BaseModel):
    """Model for ingredient response."""

    id: UUID
    name: str
    category: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
