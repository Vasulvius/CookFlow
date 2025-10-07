from typing import Dict, List, Optional, Tuple

from src.domain.entities.unit import Unit
from src.domain.repositories.unit_repository import UnitRepository


class UnitConversionService:
    """Service pour la conversion d'unités."""

    def __init__(self):
        self.unit_repository = UnitRepository()
        self._units_cache: Dict[str, Unit] = {}

    async def _load_units_cache(self):
        """Charge toutes les unités en cache."""
        if not self._units_cache:
            units = await self.unit_repository.get_all()
            self._units_cache = {unit.symbol: unit for unit in units}

    async def convert(self, value: float, from_unit: str, to_unit: str) -> Optional[float]:
        """
        Convertit une valeur d'une unité à une autre.

        Args:
            value: Valeur à convertir
            from_unit: Symbole de l'unité source
            to_unit: Symbole de l'unité cible

        Returns:
            Valeur convertie ou None si la conversion n'est pas possible
        """
        await self._load_units_cache()

        if from_unit == to_unit:
            return value

        unit_from = self._units_cache.get(from_unit)
        unit_to = self._units_cache.get(to_unit)

        if not unit_from or not unit_to:
            return None

        # On ne peut convertir que dans le même type d'unité
        if unit_from.unit_type != unit_to.unit_type:
            return None

        # Conversion via l'unité de base
        # 1. Convertir vers l'unité de base
        base_value = value * unit_from.base_conversion_factor

        # 2. Convertir de l'unité de base vers l'unité cible
        converted_value = base_value / unit_to.base_conversion_factor

        return converted_value

    async def get_compatible_units(self, unit_symbol: str) -> List[Unit]:
        """Retourne toutes les unités compatibles avec l'unité donnée."""
        await self._load_units_cache()

        unit = self._units_cache.get(unit_symbol)
        if not unit:
            return []

        return [u for u in self._units_cache.values() if u.unit_type == unit.unit_type]

    async def suggest_best_unit(self, value: float, unit_symbol: str) -> Tuple[float, str]:
        """
        Suggère la meilleure unité pour afficher une valeur.

        Args:
            value: Valeur à optimiser
            unit_symbol: Unité actuelle

        Returns:
            Tuple (nouvelle_valeur, nouveau_symbole)
        """
        await self._load_units_cache()

        unit = self._units_cache.get(unit_symbol)
        if not unit:
            return value, unit_symbol

        compatible_units = await self.get_compatible_units(unit_symbol)

        # Règles d'optimisation
        best_value, best_unit = value, unit_symbol

        for target_unit in compatible_units:
            converted_value = await self.convert(value, unit_symbol, target_unit.symbol)
            if converted_value is None:
                continue

            # Privilégier les valeurs entre 1 et 1000
            if 1 <= converted_value <= 1000:
                if abs(converted_value - 100) < abs(best_value - 100):
                    best_value, best_unit = converted_value, target_unit.symbol

        return best_value, best_unit
