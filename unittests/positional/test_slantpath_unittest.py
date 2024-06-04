import unittest
from datetime import datetime

# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj

# ====================================================
# local imports
from supportTestStructures import satPosition

from src.bindings.positional.coordinates_class import LLA_Coord
from src.bindings.positional.timeandlocation_class import TimeAndLocation
from src.positional.slantpathgenerator import SlantPathGenerator

# ====================================================
# constants
ECEF = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
LLA = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


class TestIndexOfRefractionGenerator(unittest.TestCase):

    def test_EstimateSlantPath(self):

        # Initial Starting Point
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        sat_ECEF = satPosition()

        # expected height, assume minimal change in position with range projection
        lon_deg, lat_deg, _ = pyproj.transform(
            ECEF, LLA, sat_ECEF.x_m, sat_ECEF.y_m, sat_ECEF.z_m, radians=False)

        event_LLA = LLA_Coord(lat_deg, lon_deg, 0.0)
        # construct the atmospheric model
        slantPathGenerator = SlantPathGenerator()

        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=event_LLA, eventTime_UTC=currentDateTime)

        # ======================================================
        heights_m = [0, 100, 1000, 10000, 100000, 1000000]

        rayPathPoints = slantPathGenerator.estimateSlantPath(startTimeAndLocation=timeAndLocation,
                                                             heightStratification_m=heights_m, sat_ECEF=sat_ECEF)

        self.assertEqual(len(rayPathPoints), len(heights_m) - 1)


if __name__ == '__main__':
    unittest.main()
