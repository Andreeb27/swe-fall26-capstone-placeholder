import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    scale_driver: str = "simulated"  # "simulated" | "half_decent_wifi"
    scale_ws_url: str = "ws://decent-scale.local/snapshot"  # PLACEHOLDER - confirm against HDS docs

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            scale_driver=os.getenv("SCALE_DRIVER", cls.scale_driver),
            scale_ws_url=os.getenv("SCALE_WS_URL", cls.scale_ws_url),
        )
