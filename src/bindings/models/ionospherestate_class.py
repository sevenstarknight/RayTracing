from dataclasses import dataclass


@dataclass
class IonosphereState:
    f107: float
    f107a: float
    ap: list[float]
