# ====================================================
# local imports
from src.bindings.positional.coordinates_class import ECEF_Coord
from src.bindings.raytracer.raystate_class import RayState

class RayVector:
    # Class that stores the current state (point) of the ray

    def __init__(self, rayState: RayState, sVector_m: ECEF_Coord,
                 ecef_p1: ECEF_Coord, ecef_p2: ECEF_Coord, newAltitude_m: float, n_1: complex) -> None:
        self.rayState = rayState
        self.sVector_m = sVector_m
        self.ecef_p1 = ecef_p1
        self.ecef_p2 = ecef_p2
        self.newAltitude_m = newAltitude_m
        self.n_1 = n_1
