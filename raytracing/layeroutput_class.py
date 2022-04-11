# ====================================================
# local imports
from bindings.coordinates_class import LLA


class LayerOutput:
    def __init__(self, n_1: complex, n_2: complex, entryAngle_deg: float, newAltitude_m: float, intersection_LLA: LLA, stateList: list):
        self.n_1 = n_1
        self.n_2 = n_2
        self.entryAngle_deg = entryAngle_deg
        self.newAltitude_m = newAltitude_m
        self.stateList = stateList
        self.intersection_LLA = intersection_LLA
