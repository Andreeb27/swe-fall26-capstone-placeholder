from dataclasses import dataclass


@dataclass
class HealthStatus:
    status: str
    scale_driver: str


class GetHealth:
    """Trivial example use case showing the pattern: plain class, no framework imports.

    Real use cases (DetectPour, ClassifyPour, EvaluateRules, RingInDrink...) go
    in this folder and receive ports (ScaleReader, repositories) via __init__.
    """

    def __init__(self, scale_driver: str) -> None:
        self._scale_driver = scale_driver

    def execute(self) -> HealthStatus:
        return HealthStatus(status="ok", scale_driver=self._scale_driver)
