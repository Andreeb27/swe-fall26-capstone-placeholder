from dataclasses import dataclass, field


@dataclass
class RecipeIngredient:
    name: str
    volume_oz: float
    tolerance_oz: float = 0.0
    is_monitored: bool = False  # Phase 1: only vodka is measured; mixers are not


@dataclass
class Recipe:
    name: str
    ingredients: list[RecipeIngredient] = field(default_factory=list)
