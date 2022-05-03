import math

class LLA_Coord:
    def __init__(self, lat_deg: float, lon_deg: float, altitude_m: float):
        self.lat_deg = lat_deg
        self.lon_deg = lon_deg
        self.altitude_m = altitude_m


    def setAltitude(self, newAlitude_m : float):
        self.altitude_m = newAlitude_m


class ECEF_Coord:
    def __init__(self, x_m: float, y_m: float, z_m: float):
        self.x_m = x_m
        self.y_m = y_m
        self.z_m = z_m

    def subtract(ecef1: 'ECEF_Coord', ecef2: 'ECEF_Coord') -> 'ECEF_Coord':
        return ECEF_Coord(ecef2.x_m - ecef1.x_m, ecef2.y_m - ecef1.y_m, ecef2.z_m - ecef1.z_m)

    def magnitude(self) -> float:
        return math.sqrt(self.x_m*self.x_m + self.y_m*self.y_m + self.z_m*self.z_m)
