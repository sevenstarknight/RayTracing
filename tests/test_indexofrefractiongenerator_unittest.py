import unittest
from datetime import datetime

# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj

# ====================================================
# local imports
from supportTestStructures import satPosition

from src.indexrefractionmodels.indexofrefractiongenerator import IndexOfRefractionGenerator
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel

from src.bindings import coordinates_class
from src.bindings.timeandlocation_class import TimeAndLocation

# ====================================================
# constants
ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


class TestIndexOfRefractionGenerator(unittest.TestCase):

    def test_IndexOfRefractionGenerator(self):

        # Initial Starting Point
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        sat_ECEF = satPosition()

        # expected height, assume minimal change in position with range projection
        lon_deg, lat_deg, alt_m = pyproj.transform(
            ecef, lla, sat_ECEF.x_m, sat_ECEF.y_m, sat_ECEF.z_m, radians=False)

        event_LLA = coordinates_class.LLA(lat_deg, lon_deg, 0.0)
        # construct the atmospheric model
        indexOfRefractionGenerator = IndexOfRefractionGenerator(
            frequency_hz=10e6, dispersionModel=DispersionModel.X_MODEL)

        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=event_LLA, eventTime_UTC=currentDateTime)

        # ======================================================
        heights_m = [0, 100, 1000, 10000, 100000, 1000000]

        indexNs = indexOfRefractionGenerator.estimateIndexN(startTimeAndLocation=timeAndLocation,
                                                            heightStratification_m=heights_m, sat_ECEF=sat_ECEF)

        self.assertEqual(len(indexNs), len(heights_m))


if __name__ == '__main__':
    unittest.main()
