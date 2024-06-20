import unittest
from datetime import datetime

# ====================================================
# local imports
from src.positional.locationconverter_computations import LocationConverterComputation
from supportTestStructures import satPosition

from src.bindings.positional.coordinates_class import LLA_Coord
from src.bindings.positional.timeandlocation_class import TimeAndLocation
from src.positional.slantpathgenerator import SlantPathGenerator



class TestIndexOfRefractionGenerator(unittest.TestCase):

    def test_EstimateSlantPath(self):

        # Initial Starting Point
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        sat_ECEF = satPosition()

        # expected height, assume minimal change in position with range projection
        event_LLA: LLA_Coord = LocationConverterComputation.convertFromECEFtoLLA(ecef=sat_ECEF)
        event_LLA.setAltitude(0.0)
        
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
