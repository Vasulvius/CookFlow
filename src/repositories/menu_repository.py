from src.entities.menu import Menu

from .base_repository import BaseRepository


class MenuRepository(BaseRepository[Menu]):
    """Repository to manage CRUD operations on menus."""

    def __init__(self):
        super().__init__(Menu)
