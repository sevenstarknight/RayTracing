# STDLIB modules
from dataclasses import dataclass

# FIRSTPARTY modules
from src.bindings.positional.coordinates_class import ECEF_Coord
from src.bindings.raytracer.raystate_class import RayState


@dataclass
class RayVector:
    # Class that stores the current state (point) of the ray
    rayState: RayState
    sVector_m: ECEF_Coord
    ecef_p1: ECEF_Coord
    ecef_p2: ECEF_Coord
    newAltitude_m: float
    n_1: complex
