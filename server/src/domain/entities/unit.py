from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class UnitType(str, Enum):
    """Types d'unités."""

    VOLUME = "volume"
    WEIGHT = "weight"
    QUANTITY = "quantity"


class Unit(SQLModel, table=True):
    """Entité Unit avec SQLModel."""

    __tablename__ = "units"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=50, unique=True)
    symbol: str = Field(max_length=10, unique=True)
    unit_type: UnitType = Field(description="Type d'unité")
    base_conversion_factor: float = Field(description="Facteur de conversion vers l'unité de base")
    is_base_unit: bool = Field(default=False, description="Si c'est l'unité de base pour son type")


class UnitCreate(SQLModel):
    name: str = Field(max_length=50)
    symbol: str = Field(max_length=10)
    unit_type: UnitType
    base_conversion_factor: float
    is_base_unit: bool = False


class UnitRead(SQLModel):
    id: UUID
    name: str
    symbol: str
    unit_type: UnitType
    base_conversion_factor: float
    is_base_unit: bool


class UnitUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=50)
    symbol: Optional[str] = Field(default=None, max_length=10)
    unit_type: Optional[UnitType] = None
    base_conversion_factor: Optional[float] = None
    is_base_unit: Optional[bool] = None
