from abc import ABC, abstractmethod

from fastapi import APIRouter


class AbstractRouter(ABC):
    def __init__(self, prefix: str = "", tags: list[str] = []):
        self.prefix = prefix
        self.tags = tags
        self.router = APIRouter(prefix=self.prefix, tags=self.tags)
        self._register_routes()

    @abstractmethod
    def _register_routes(self):
        pass
