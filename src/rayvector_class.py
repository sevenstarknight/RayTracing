# ====================================================
# local imports
from src.bindings.coordinates_class import ECEF_Coord
from src.raystate_class import RayState


class RayVector:
    # Class that stores the current state (point) of the ray

    def __init__(self, rayState: RayState, sVector_m :ECEF_Coord, 
    ecef_p1 : ECEF_Coord, ecef_p2: ECEF_Coord, newAltitude_m: float, n_1 : complex) -> None:
        self._rayState = rayState
        self._sVector_m = sVector_m
        self._ecef_p1 = ecef_p1
        self._ecef_p2 = ecef_p2
        self._newAltitude_m = newAltitude_m
        self._n_1 = n_1