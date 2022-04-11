import unittest
# https://pyproj4.github.io/pyproj/stable/
import pyproj
from datetime import datetime

# ====================================================
# local imports
from raytracing.bindings.coordinates_class import LLA
from raytracing.bindings.timeandlocation_class import TimeAndLocation
from raytracing.bindings.satelliteinformation_class import SatelliteInformation
from raytracing.indexrefractionmodels.dispersionmodels_enum import DispersionModel

from raytracing.satellitepositiongenerator import SatellitePositionGenerator
from raytracing.raypathoptimizer import RayPathOptimizer

ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


class TestRayPathOptimization(unittest.TestCase):

    def test_RayPathOptimization(self):

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
            ecef, lla, sat_ECEF.x_m, sat_ECEF.y_m, sat_ECEF.z_m, radians=False)

        event_LLA = LLA(lat_deg, lon_deg, 0.0)
        timeAndLocation = TimeAndLocation(
            eventTime_UTC=currentDateTime, eventLocation_LLA=event_LLA)
        # ======================================================
        heights_m = [0, 100, 1000, 10000, 100000, 1000000]

        optimizer = RayPathOptimizer(
            10e6, timeAndLocation, heights_m, dispersionModel=DispersionModel.X_MODEL)
        rayState = optimizer.optimize(satelliteInformation)

        self.assertTrue(rayState is not None)


if __name__ == '__main__':
    unittest.main()
