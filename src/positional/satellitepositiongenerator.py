from datetime import datetime

# ====================================================
# https://rhodesmill.org/skyfield/
from skyfield.api import EarthSatellite
from skyfield.api import load
from skyfield.framelib import itrs

# ====================================================
# local imports
from src.bindings.positional.coordinates_class import ECEF_Coord
from src.bindings.positional.satelliteinformation_class import SatelliteInformation


class SatellitePositionGenerator:
    def __init__(self, satelliteInformation: SatelliteInformation):
        self.satelliteInformation = satelliteInformation
        self.ts = load.timescale()
        self.satellite = EarthSatellite(
            line1=satelliteInformation.s,
            line2=satelliteInformation.t,
            name=satelliteInformation.name,
            ts=self.ts,
        )

    def estimatePosition_ECEF(self, currentDateTime: datetime) -> ECEF_Coord:

        t = self.ts.utc(
            year=currentDateTime.year,
            month=currentDateTime.month,
            day=currentDateTime.day,
            hour=currentDateTime.hour,
            minute=currentDateTime.minute,
            second=currentDateTime.second,
        )
        variable = self.satellite.at(t)

        x, y, z = variable.frame_xyz(itrs).m

        return ECEF_Coord(x_m=x, y_m=y, z_m=z)
