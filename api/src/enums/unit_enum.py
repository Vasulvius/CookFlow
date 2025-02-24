from enum import Enum


class UnitEnum(str, Enum):
    gram = "g"
    kilogram = "kg"
    milliliter = "ml"
    centiliter = "cl"
    liter = "l"
    piece = "piece"
    tablespoon = "tbsp"
    teaspoon = "tsp"
