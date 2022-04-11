import unittest
# https://pyproj4.github.io/pyproj/stable/
import pyproj
from datetime import datetime

from raytracing.bindings import coordinates_class
from raytracing.bindings.satelliteinformation_class import SatelliteInformation
from raytracing.bindings.timeandlocation_class import TimeAndLocation
from raytracing.satellitepositiongenerator import SatellitePositionGenerator
from raytracing.slantpathgenerator import SlantPathGenerator
from tests.supportTestStructures import satPosition

ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


class TestIndexOfRefractionGenerator(unittest.TestCase):

    def test_EstimateSlantPath(self):

        # Initial Starting Point
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        sat_ECEF = satPosition()

        # expected height, assume minimal change in position with range projection
        lon_deg, lat_deg, alt_m = pyproj.transform(
            ecef, lla, sat_ECEF.x_m, sat_ECEF.y_m, sat_ECEF.z_m, radians=False)

        event_LLA = coordinates_class.LLA(lat_deg, lon_deg, 0.0)
        # construct the atmospheric model
        slantPathGenerator = SlantPathGenerator()

        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=event_LLA, eventTime_UTC=currentDateTime)

        # ======================================================
        heights_m = [0, 100, 1000, 10000, 100000, 1000000]

        rayPathPoints = slantPathGenerator.estimateSlantPath(startTimeAndLocation=timeAndLocation,
                                                             heightStratification_m=heights_m, sat_ECEF=sat_ECEF)

        self.assertEqual(len(rayPathPoints), len(heights_m))


if __name__ == '__main__':
    unittest.main()
