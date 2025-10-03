from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.entities.menu import Menu, MenuCreate, MenuRead, MenuUpdate
from src.repositories.menu_repository import MenuRepository
from src.repositories.recipe_repository import RecipeRepository

router = APIRouter()
menu_repository = MenuRepository()
recipe_repository = RecipeRepository()


@router.post("/", response_model=MenuRead)
async def create_menu(menu_create: MenuCreate):
    """Create a new menu."""
    try:
        # Validate that all recipe IDs exist using the exists method
        if menu_create.recipe_ids:
            for recipe_id_str in menu_create.recipe_ids:
                try:
                    recipe_uuid = UUID(recipe_id_str)
                    if not await recipe_repository.exists(recipe_uuid):
                        raise HTTPException(status_code=400, detail=f"Recipe with ID {recipe_id_str} not found")
                except ValueError:
                    raise HTTPException(status_code=400, detail=f"Invalid UUID format: {recipe_id_str}")

        menu_data = menu_create.model_dump()
        menu = Menu.model_validate(menu_data)
        created_menu = await menu_repository.add(menu)
        return created_menu
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[MenuRead])
async def read_menus():
    """Retrieve all menus."""
    return await menu_repository.get_all()


@router.get("/{menu_id}", response_model=MenuRead)
async def read_menu(menu_id: UUID):
    """Retrieve a menu by its ID."""
    menu = await menu_repository.get_by_id(menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu


@router.put("/{menu_id}", response_model=MenuRead)
async def update_menu(menu_id: UUID, menu_update: MenuUpdate):
    """Update an existing menu."""
    try:
        # Validate recipe IDs if they are being updated
        if menu_update.recipe_ids is not None:
            for recipe_id_str in menu_update.recipe_ids:
                try:
                    recipe_uuid = UUID(recipe_id_str)
                    if not await recipe_repository.exists(recipe_uuid):
                        raise HTTPException(status_code=400, detail=f"Recipe with ID {recipe_id_str} not found")
                except ValueError:
                    raise HTTPException(status_code=400, detail=f"Invalid UUID format: {recipe_id_str}")

        # Get existing menu
        existing_menu = await menu_repository.get_by_id(menu_id)
        if not existing_menu:
            raise HTTPException(status_code=404, detail="Menu not found")

        # Update fields
        update_data = menu_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing_menu, field, value)

        updated_menu = await menu_repository.update(existing_menu)
        return updated_menu
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{menu_id}")
async def delete_menu(menu_id: UUID):
    """Delete a menu by its ID."""
    try:
        await menu_repository.delete(menu_id)
        return {"detail": "Menu successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
