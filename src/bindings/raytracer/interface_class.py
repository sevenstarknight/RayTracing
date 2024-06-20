# FIRSTPARTY modules
from src.bindings.positional.coordinates_class import LLA_Coord


class Interface:
    def __init__(
        self,
        n_1: complex,
        n_2: complex,
        entryAngle_deg: float,
        newAltitude_m: float,
        intersection_LLA: LLA_Coord,
    ):
        self.n_1 = n_1
        self.n_2 = n_2
        self.entryAngle_deg = entryAngle_deg
        self.newAltitude_m = newAltitude_m
        self.intersection_LLA = intersection_LLA

    @classmethod
    def from_Empty(cls):
        return cls(
            n_1=None,
            n_2=None,
            entryAngle_deg=None,
            newAltitude_m=None,
            intersection_LLA=None,
        )
