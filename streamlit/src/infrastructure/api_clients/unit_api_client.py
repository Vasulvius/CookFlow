import httpx
from src.domain.entities.unit import Unit


class UnitAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_units(self) -> list[Unit]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/units/")
            response.raise_for_status()
            data = response.json()
            return [Unit(**item) for item in data]

    async def create_unit(self, name: str, symbol: str, unit_type: str, base_conversion_factor: float, is_base_unit: bool = False) -> Unit:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            payload = {
                "name": name,
                "symbol": symbol,
                "unit_type": unit_type,
                "base_conversion_factor": base_conversion_factor,
                "is_base_unit": is_base_unit,
            }
            response = await client.post(f"{self.base_url}/units/", json=payload)
            response.raise_for_status()
            data = response.json()
            return Unit(**data)

    async def convert_units(self, value: float, from_unit: str, to_unit: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/units/convert", params={"value": value, "from_unit": from_unit, "to_unit": to_unit}
            )
            response.raise_for_status()
            return response.json()
