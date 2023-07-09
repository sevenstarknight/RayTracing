
from dataclasses import dataclass

from src.bindings.positional.coordinates_class import ECEF_Coord

@dataclass
class IntersectionPoint():
    ecef_p2 : ECEF_Coord
    newAltitude_m : float
    indx : int