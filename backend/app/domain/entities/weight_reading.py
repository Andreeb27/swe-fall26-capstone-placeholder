from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class WeightReading:
    """One raw reading from any scale, normalized to grams."""

    grams: float
    timestamp: datetime
