from abc import ABC, abstractmethod

from app.domain.entities.pour_event import PourEvent
from app.domain.entities.recipe import Recipe


class PourEventRepository(ABC):
    @abstractmethod
    def add(self, event: PourEvent) -> None: ...

    @abstractmethod
    def list_recent(self, limit: int = 50) -> list[PourEvent]: ...


class RecipeRepository(ABC):
    @abstractmethod
    def get(self, name: str) -> Recipe | None: ...

    @abstractmethod
    def list_all(self) -> list[Recipe]: ...

    @abstractmethod
    def save(self, recipe: Recipe) -> None: ...

    @abstractmethod
    def delete(self, name: str) -> None: ...
