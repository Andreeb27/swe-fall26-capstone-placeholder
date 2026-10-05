from app.domain.ports.scale_port import ScaleReader
from app.infrastructure.config import Settings
from app.infrastructure.scale.half_decent_wifi_scale import HalfDecentWifiScale
from app.infrastructure.scale.simulated_scale import SimulatedScale


def build_scale(settings: Settings) -> ScaleReader:
    """Pick the scale adapter from config. Add new hardware here."""
    if settings.scale_driver == "half_decent_wifi":
        return HalfDecentWifiScale(settings.scale_ws_url)
    if settings.scale_driver == "simulated":
        return SimulatedScale()
    raise ValueError(f"Unknown SCALE_DRIVER: {settings.scale_driver!r}")
