from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.domain.entities.weight_reading import WeightReading


class ScaleReader(ABC):
    """Port for any scale (WiFi Half Decent Scale, USB, simulated...).

    The rest of the app depends only on this interface, so swapping hardware
    means writing one new adapter in infrastructure/scale/.
    """

    @abstractmethod
    def stream(self) -> AsyncIterator[WeightReading]:
        """Yield live weight readings (implement as an async generator)."""

    @abstractmethod
    async def tare(self) -> None:
        """Zero the scale."""
