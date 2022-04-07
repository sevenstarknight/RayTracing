## ====================================================
# local imports
from bindings.coordinates_class import LLA

class RayState:
    # Class that stores the current state (point) of the ray
    
    def __init__(self, exitElevation_deg : float, exitAzimuth_deg : float, lla : LLA, nIndex : complex):
        self.exitElevation_deg = exitElevation_deg
        self.exitAzimuth_deg = exitAzimuth_deg
        self.lla = lla
        self.nIndex = nIndex

    def generateList(self):
        return([self.exitElevation_deg,self.exitAzimuth_deg, self.lla.lat_deg, self.lla.lon_deg, self.lla.altitude_m, self.nIndex])

    def generateColumnNames(self):
        return(["Exit Elevation", "Exit Azimuth", "Latitude", "Longitude", "Altitude", "n"])

    def isNone(self):
        #attrs = vars(self)
        #print(', '.join("%s: %s" % item for item in attrs.items()))

        filledUp = self.exitElevation_deg is None
        filledUp = filledUp & self.exitAzimuth_deg is None
        filledUp = filledUp & self.lla.lat_deg is None
        filledUp = filledUp & self.lla.lon_deg is None
        filledUp = filledUp & self.lla.altitude_m is None
        filledUp = filledUp & self.nIndex is None

        return(filledUp)