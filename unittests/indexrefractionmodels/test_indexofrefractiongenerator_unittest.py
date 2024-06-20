import unittest
from datetime import datetime


# FIRSTPARTY modules
from src.positional.locationconverter_computations import LocationConverterComputation
from src.indexrefractionmodels.indexofrefractiongenerator import IndexOfRefractionGenerator
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.bindings.models.ionospherestate_class import IonosphereState
from src.bindings.positional.coordinates_class import LLA_Coord
from src.bindings.positional.timeandlocation_class import TimeAndLocation
from unittests.testutilities import TestUtilities


class TestIndexOfRefractionGenerator(unittest.TestCase):

    def test_IndexOfRefractionGenerator(self):

        # Initial Starting Point
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        sat_ECEF = TestUtilities.satPosition()

        # expected height, assume minimal change in position with range projection
        event_LLA: LLA_Coord = LocationConverterComputation.convertFromECEFtoLLA(ecef=sat_ECEF)
        event_LLA.setAltitude(0.0)

        ionosphereState = IonosphereState(10.0, 10.0, 3.0)
        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=event_LLA, eventTime_UTC=currentDateTime)
        # construct the atmospheric model
        indexOfRefractionGenerator = IndexOfRefractionGenerator(
            frequency_hz=1000e6, dispersionModel=DispersionModel.X_MODEL, transportMode=TransportMode.PLASMA_MODE,
            startTimeAndLocation=timeAndLocation,ionosphereState = ionosphereState)


        # ======================================================
        heights_m = [0, 100, 1000, 10000, 100000, 1000000]

        indexNs = indexOfRefractionGenerator.estimateIndexN(
                                                            heightStratification_m=heights_m, 
                                                            sat_ECEF=sat_ECEF)

        self.assertEqual(len(indexNs), len(heights_m))


if __name__ == '__main__':
    unittest.main()
