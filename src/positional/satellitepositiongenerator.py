
from datetime import datetime

# ====================================================
# https://rhodesmill.org/skyfield/
from skyfield.api import EarthSatellite
from skyfield.api import load
from skyfield.framelib import itrs

# ====================================================
# local imports
from src.bindings.coordinates_class import ECEF_Coord
from src.bindings.satelliteinformation_class import SatelliteInformation


class SatellitePositionGenerator():
    def __init__(self, satelliteInformation: SatelliteInformation):
        self.satelliteInformation = satelliteInformation
        self.ts = load.timescale()
        self.satellite = EarthSatellite(satelliteInformation.s, satelliteInformation.t,
                                        satelliteInformation.name, self.ts)

    def estimatePosition_ECEF(self, currentDateTime: datetime) -> ECEF_Coord:
        currentDateTime.year
        t = self.ts.utc(currentDateTime.year, currentDateTime.month, currentDateTime.day,
                        currentDateTime.hour, currentDateTime.minute, currentDateTime.second)
        variable = self.satellite.at(t)

        x, y, z = variable.frame_xyz(itrs).m

        return(ECEF_Coord(x, y, z))
