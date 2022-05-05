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
from src.indexrefractionmodels.transportmodes_enum import TransportMode

from src.bindings.ionospherestate_class import IonosphereState
from src.bindings.coordinates_class import LLA_Coord
from src.bindings.timeandlocation_class import TimeAndLocation

# ====================================================
# constants
ECEF = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
LLA = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


class TestIndexOfRefractionGenerator(unittest.TestCase):

    def test_IndexOfRefractionGenerator(self):

        # Initial Starting Point
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        sat_ECEF = satPosition()

        # expected height, assume minimal change in position with range projection
        lon_deg, lat_deg, alt_m = pyproj.transform(
            ECEF, LLA, sat_ECEF.x_m, sat_ECEF.y_m, sat_ECEF.z_m, radians=False)

        event_LLA = LLA_Coord(lat_deg, lon_deg, 0.0)
        # construct the atmospheric model
        indexOfRefractionGenerator = IndexOfRefractionGenerator(
            frequency_hz=10e6, dispersionModel=DispersionModel.X_MODEL, transportMode=TransportMode.PLASMA_MODE)

        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=event_LLA, eventTime_UTC=currentDateTime)

        # ======================================================
        heights_m = [0, 100, 1000, 10000, 100000, 1000000]
        ionosphereState = IonosphereState(10.0, 10.0, 3.0)

        indexNs = indexOfRefractionGenerator.estimateIndexN(startTimeAndLocation=timeAndLocation,
                                                            heightStratification_m=heights_m, 
                                                            sat_ECEF=sat_ECEF, ionosphereState = ionosphereState)

        self.assertEqual(len(indexNs), len(heights_m))


if __name__ == '__main__':
    unittest.main()
