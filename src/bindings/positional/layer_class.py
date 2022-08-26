
from src.bindings.positional.coordinates_class import AER_Coord, ECEF_Coord, LLA_Coord


class Layer():

    def __init__(self, lla : LLA_Coord, 
                 ecef_p1: ECEF_Coord, ecef_p2: ECEF_Coord, newAltitude_m: float, 
                 aer : AER_Coord) -> None:

        self.ecef_p1 = ecef_p1
        self.ecef_p2 = ecef_p2
        self.lla = lla
        self.newAltitude_m = newAltitude_m
        self.aer = aer
