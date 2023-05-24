from dataclasses import dataclass
from src.bindings.positional.coordinates_class import AER_Coord, ECEF_Coord, LLA_Coord


@dataclass
class Layer:
    ecef_p1: ECEF_Coord
    ecef_p2: ECEF_Coord
    lla: LLA_Coord
    newAltitude_m: float
    aer: AER_Coord
