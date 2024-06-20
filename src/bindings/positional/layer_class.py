# STDLIB modules
from dataclasses import dataclass

# FIRSTPARTY modules
from src.bindings.positional.coordinates_class import AER_Coord, ECEF_Coord, LLA_Coord


@dataclass
class Layer:
    ecef_p1: ECEF_Coord # Bottom of the Layer @ entry
    ecef_p2: ECEF_Coord # Top of the Layer @ Exit
    lla_p1: LLA_Coord # Bottom of the Layer LLA
    lla_p2: LLA_Coord # Top of the Layer Altitude
    aer: AER_Coord # The AER Vector
