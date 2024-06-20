# STDLIB modules
import math
from dataclasses import dataclass


@dataclass
class ENU_Coord:
    e_m: float
    n_m: float
    u_m: float


@dataclass
class AER_Coord:
    az_deg: float
    ele_deg: float
    range_m: float


@dataclass
class LLA_Coord:
    lat_deg: float
    lon_deg: float
    altitude_m: float

    def setAltitude(self, newAlitude_m: float):
        self.altitude_m = newAlitude_m


@dataclass
class ECEF_Coord:
    x_m: float
    y_m: float
    z_m: float

    def subtract(ecef1: "ECEF_Coord", ecef2: "ECEF_Coord") -> "ECEF_Coord":
        return ECEF_Coord(
            ecef2.x_m - ecef1.x_m, ecef2.y_m - ecef1.y_m, ecef2.z_m - ecef1.z_m
        )

    def magnitude(self) -> float:
        return math.sqrt(
            self.x_m * self.x_m + self.y_m * self.y_m + self.z_m * self.z_m
        )
