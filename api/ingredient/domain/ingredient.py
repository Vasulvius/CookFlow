from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Ingredient:
    """Ingredient domain entity."""

    id: UUID
    name: str
    category: Optional[str]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dict(cls, data: dict) -> "Ingredient":
        """Create an Ingredient from a dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            category=data.get("category"),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )
