import unittest
from datetime import datetime

# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj

# ====================================================
# local imports
from src.bindings.coordinates_class import LLA_Coord
from src.bindings.timeandlocation_class import TimeAndLocation
from src.bindings.satelliteinformation_class import SatelliteInformation
from src.indexrefractionmodels.indexofrefractiongenerator import IndexOfRefractionGenerator
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.positional.satellitepositiongenerator import SatellitePositionGenerator
from src.raytracer.raypathobjective import RayPathObjective

# ====================================================
# constants
ECEF = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
LLA = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


class TestRayPathObjective(unittest.TestCase):

    def test_RayPathObjective(self):

        s = '1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991'
        t = '2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482'
        name = "Test"

        satelliteInformation = SatelliteInformation(name=name, s=s, t=t)
        # Initial Starting Point
        satPosGenerator = SatellitePositionGenerator(satelliteInformation)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        sat_ECEF = satPosGenerator.estimatePosition_ECEF(currentDateTime)

        # expected height, assume minimal change in position with range projection
        lon_deg, lat_deg, alt_m = pyproj.transform(
            ECEF, LLA, sat_ECEF.x_m, sat_ECEF.y_m, sat_ECEF.z_m, radians=False)

        event_LLA = LLA_Coord(lat_deg, lon_deg, 0.0)

        # ======================================================
        heights_m = [0, 100, 1000, 10000, 100000, 1000000]
        timeAndLocation = TimeAndLocation(
            eventTime_UTC=currentDateTime, eventLocation_LLA=event_LLA)

        indexOfRefractionGenerator = IndexOfRefractionGenerator(
            frequency_hz=10e6, dispersionModel=DispersionModel.X_MODEL, transportMode=TransportMode.PLASMA_MODE)

        rayPathOpt = RayPathObjective(freq_hz=10e6,
                                      heights_m=heights_m, timeAndLocation=timeAndLocation, satPosGen=satPosGenerator, indexOfRefractionGenerator=indexOfRefractionGenerator)

        param = [80, 10]
        loss = rayPathOpt.objectiveFunction(param)

        self.assertTrue(loss is not None)


if __name__ == '__main__':
    unittest.main()
