from uuid import UUID

from fastapi import APIRouter, HTTPException
from src.application.services import UnitConversionService
from src.domain.entities.unit import Unit, UnitCreate, UnitRead, UnitUpdate
from src.domain.repositories.unit_repository import UnitRepository

router = APIRouter()
unit_repository = UnitRepository()


@router.get("/", response_model=list[UnitRead])
async def get_units():
    """Récupère toutes les unités."""
    return await unit_repository.get_all()


@router.post("/", response_model=UnitRead, status_code=201)
async def create_unit(unit_create: UnitCreate):
    """Crée une nouvelle unité."""
    # Convertir UnitCreate en Unit
    unit = Unit(**unit_create.model_dump())
    return await unit_repository.add(unit)


@router.get("/{unit_id}", response_model=UnitRead)
async def get_unit(unit_id: UUID):
    """Récupère une unité par son ID."""
    unit = await unit_repository.get_by_id(unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit


@router.put("/{unit_id}", response_model=UnitRead)
async def update_unit(unit_id: UUID, unit_update: UnitUpdate):
    """Met à jour une unité."""
    # Récupérer l'unité existante
    existing_unit = await unit_repository.get_by_id(unit_id)
    if not existing_unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    # Mettre à jour les champs modifiés
    update_data = unit_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_unit, field, value)

    return await unit_repository.update(existing_unit)


@router.delete("/{unit_id}")
async def delete_unit(unit_id: UUID):
    """Supprime une unité."""
    success = await unit_repository.delete(unit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Unit not found")
    return {"message": "Unit deleted successfully"}


@router.get("/compatible/{unit_symbol}")
async def get_compatible_units(unit_symbol: str):
    """Récupère les unités compatibles pour conversion."""
    conversion_service = UnitConversionService()
    return await conversion_service.get_compatible_units(unit_symbol)


@router.post("/convert")
async def convert_units(value: float, from_unit: str, to_unit: str):
    """Convertit une valeur d'une unité à une autre."""
    conversion_service = UnitConversionService()
    result = await conversion_service.convert(value, from_unit, to_unit)
    if result is None:
        raise HTTPException(status_code=400, detail="Conversion not possible")
    return {"original_value": value, "converted_value": result, "from_unit": from_unit, "to_unit": to_unit}
