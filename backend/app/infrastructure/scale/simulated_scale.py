import asyncio
import random
from collections.abc import AsyncIterator
from datetime import datetime, timezone

from app.domain.entities.weight_reading import WeightReading
from app.domain.ports.scale_port import ScaleReader


class SimulatedScale(ScaleReader):
    """Fake scale for development without hardware: a steady bottle weight plus noise."""

    def __init__(self, base_grams: float = 1200.0, interval_s: float = 0.1) -> None:
        self._base = base_grams
        self._tare_offset = 0.0
        self._interval = interval_s

    async def stream(self) -> AsyncIterator[WeightReading]:
        while True:
            noise = random.uniform(-0.3, 0.3)
            yield WeightReading(
                grams=self._base - self._tare_offset + noise,
                timestamp=datetime.now(timezone.utc),
            )
            await asyncio.sleep(self._interval)

    async def tare(self) -> None:
        self._tare_offset = self._base
