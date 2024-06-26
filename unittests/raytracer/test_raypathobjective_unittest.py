# STDLIB modules
import unittest
from datetime import datetime


# FIRSTPARTY modules
from src.bindings.positional.coordinates_class import LLA_Coord
from src.bindings.models.ionospherestate_class import IonosphereState
from src.bindings.positional.timeandlocation_class import TimeAndLocation
from src.bindings.positional.satelliteinformation_class import SatelliteInformation
from src.indexrefractionmodels.indexofrefractiongenerator import IndexOfRefractionGenerator
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.positional.locationconverter_computations import LocationConverterComputation
from src.positional.satellitepositiongenerator import SatellitePositionGenerator
from src.raytracer.raypathobjective import RayPathObjective


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

        ionosphereState = IonosphereState(10.0, 10.0, 3.0)

        # expected height, assume minimal change in position with range projection
        event_LLA: LLA_Coord = LocationConverterComputation.convertFromECEFtoLLA(ecef=sat_ECEF)
        event_LLA.setAltitude(0.0)

        # ======================================================
        heights_m = [0, 100, 1000, 10000, 100000, 1000000]
        timeAndLocation = TimeAndLocation(
            eventTime_UTC=currentDateTime, eventLocation_LLA=event_LLA)

        indexOfRefractionGenerator = IndexOfRefractionGenerator(
            frequency_hz=1000e6, dispersionModel=DispersionModel.X_MODEL, transportMode=TransportMode.PLASMA_MODE,
            startTimeAndLocation=timeAndLocation, ionosphereState=ionosphereState)

        rayPathOpt = RayPathObjective(heights_m=heights_m,
                                      timeAndLocation=timeAndLocation, satPosGen=satPosGenerator,
                                      indexOfRefractionGenerator=indexOfRefractionGenerator)

        param = [80, 10]
        loss = rayPathOpt.objectiveFunction(param)

        self.assertTrue(loss is not None)


if __name__ == '__main__':
    unittest.main()
