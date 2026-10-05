from dataclasses import dataclass
from datetime import datetime


@dataclass
class PourEvent:
    """Standardized pour event (see sponsor spec, section 4). Data only, no logic yet."""

    timestamp: datetime
    bartender_id: str
    bartender_name: str
    station_id: str
    bottle_id: str
    recipe_name: str
    recipe_volume_oz: float
    actual_volume_oz: float
    pos_ticket_id: str | None = None
    is_spill: bool = False
    is_waste: bool = False
    waste_reason: str | None = None
