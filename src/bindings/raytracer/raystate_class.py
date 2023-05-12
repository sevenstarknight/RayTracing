from dataclasses import dataclass
# ====================================================
# local imports
from src.bindings.positional.coordinates_class import LLA_Coord

@dataclass
class RayState:
    # Class that stores the current state (point) of the ray
    exitElevation_deg : float
    exitAzimuth_deg : float
    lla : LLA_Coord

    def generateList(self):
        return([self.exitElevation_deg, self.exitAzimuth_deg, self.lla.lat_deg, self.lla.lon_deg,
                self.lla.altitude_m])

    def generateColumnNames(self):
        return(["Exit Elevation", "Exit Azimuth", "Latitude", "Longitude", "Altitude"])

    def isNone(self):

        filledUp = self.exitElevation_deg is None
        filledUp = filledUp & self.exitAzimuth_deg is None
        filledUp = filledUp & self.lla.lat_deg is None
        filledUp = filledUp & self.lla.lon_deg is None
        filledUp = filledUp & self.lla.altitude_m is None

        return(filledUp)
