from dataclasses import dataclass
from uuid import UUID


@dataclass
class Unit:
    id: UUID
    name: str
    symbol: str
    unit_type: str
    base_conversion_factor: float
    is_base_unit: bool
