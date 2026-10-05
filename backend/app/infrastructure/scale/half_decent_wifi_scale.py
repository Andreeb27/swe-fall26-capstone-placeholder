from collections.abc import AsyncIterator

from app.domain.entities.weight_reading import WeightReading
from app.domain.ports.scale_port import ScaleReader


class HalfDecentWifiScale(ScaleReader):
    """Adapter for the Half Decent Scale over WiFi (firmware 3.0.0+ exposes weight via WebSocket).

    STUB. TODO for the hardware owner, once the scale is on the same network:
      1. Confirm the WebSocket URL/path/port and message format in the Decent docs
         (https://decentespresso.com/docs/firmware_for_half_decent_scale) or the
         firmware repo (github.com/decentespresso/openscale).
      2. Implement _parse() to turn one message into a WeightReading (grams).
      3. Implement tare() using the tare command from those docs.
    """

    def __init__(self, ws_url: str) -> None:
        self._ws_url = ws_url

    async def stream(self) -> AsyncIterator[WeightReading]:
        import websockets  # imported lazily so the app runs without hardware

        async with websockets.connect(self._ws_url) as ws:
            async for message in ws:
                yield self._parse(message)

    async def tare(self) -> None:
        raise NotImplementedError("Send the tare command per the Half Decent Scale docs.")

    def _parse(self, message: str | bytes) -> WeightReading:
        raise NotImplementedError("Message format not yet confirmed; see class docstring.")
