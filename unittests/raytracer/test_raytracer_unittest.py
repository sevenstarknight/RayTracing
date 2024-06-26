# STDLIB modules
import unittest
from datetime import datetime

# FIRSTPARTY modules
from src.bindings.raytracer.interface_class import Interface
from src.bindings.positional.coordinates_class import LLA_Coord
from src.bindings.positional.timeandlocation_class import TimeAndLocation
from src.raytracer.raytracer import RayTracer, TransitionGenerator, TransitionOutput
from src.bindings.raytracer.raystate_class import RayState

class TestRayTracer(unittest.TestCase):

    def setUp(self):
        self.heights_m = [0, 100, 1000, 10000, 100000, 1000000]
        self.indexNs = [1.0, 1.0, 0.95, 0.95, 0.97, 1.0]
        self.initialAzimuth_deg = 0.0

    def test_raytracer(self):

        # initial structure
        initialElevationAngle_deg = 45.0
        initialLLA = LLA_Coord(0.0, 0.0, 0.0)

        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=initialLLA, eventTime_UTC=currentDateTime
        )
        rayTracer = RayTracer(timeAndLocation=timeAndLocation,
                              heights_m=self.heights_m, indexNs=self.indexNs)
        stateList = rayTracer.execute(
            params=[self.initialAzimuth_deg, initialElevationAngle_deg])
        self.assertEqual(len(stateList), len(self.heights_m) - 1)

    # ============================================================================

    def test_insideLayerOperations_out(self):
        # initial structure
        initialElevationAngle_deg = 45.0
        initialLLA = LLA_Coord(0.0, 0.0, 1000000.0)
        initialNIndex = 1.0

        initialState = RayState(exitElevation_deg=initialElevationAngle_deg, exitAzimuth_deg=self.initialAzimuth_deg,
                                lla=initialLLA)

        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=initialLLA, eventTime_UTC=currentDateTime
        )

        transitionGenerator = TransitionGenerator(
            heights_m=self.heights_m, indexNs=self.indexNs, timeAndLocation=timeAndLocation, currentState=initialState)
        
        transitionOutput : TransitionOutput = transitionGenerator.insideLayerOperations(
            currentRayState=initialState)

        self.assertEqual(transitionOutput, None)

    def test_insideLayerOperations_up(self):

        # initial structure
        initialElevationAngle_deg = 45.0
        initialLLA = LLA_Coord(0.0, 0.0, 0.0)
        initialNIndex = 1.0

        initialState = RayState(exitElevation_deg=initialElevationAngle_deg, exitAzimuth_deg=self.initialAzimuth_deg,
                                lla=initialLLA)

        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=initialLLA, eventTime_UTC=currentDateTime
        )

        transitionGenerator = TransitionGenerator(
            heights_m=self.heights_m, indexNs=self.indexNs, timeAndLocation=timeAndLocation, currentState=initialState)
        
        transitionOutput : TransitionOutput = transitionGenerator.insideLayerOperations(
            currentRayState=initialState)

        self.assertEqual(transitionOutput.interface.newAltitude_m, 100)
        self.assertEqual(transitionOutput.interface.n_2, 1.0)

    def test_insideLayerOperations_down(self):

        # initial structure
        initialElevationAngle_deg = -45.0
        initialLLA = LLA_Coord(0.0, 0.0, 9000.0)
        initialNIndex = 0.95

        initialState = RayState(exitElevation_deg=initialElevationAngle_deg, exitAzimuth_deg=self.initialAzimuth_deg,
                                lla=initialLLA)

        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=initialLLA, eventTime_UTC=currentDateTime
        )

        transitionGenerator = TransitionGenerator(
            heights_m=self.heights_m, indexNs=self.indexNs, timeAndLocation=timeAndLocation, currentState=initialState)
        
        transitionOutput : TransitionOutput = transitionGenerator.insideLayerOperations(
            currentRayState=initialState)

        self.assertEqual(transitionOutput.interface.newAltitude_m, 1000)
        self.assertEqual(transitionOutput.interface.n_2, 1.0)

    def test_insideLayerOperations_bounce(self):
        # initial structure
        initialElevationAngle_deg = -80.0
        initialLLA = LLA_Coord(0.0, 0.0, 10.0)
        initialNIndex = 1.0

        initialState = RayState(exitElevation_deg=initialElevationAngle_deg, exitAzimuth_deg=self.initialAzimuth_deg,
                                lla=initialLLA)

        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=initialLLA, eventTime_UTC=currentDateTime
        )

        transitionGenerator = TransitionGenerator(
            heights_m=self.heights_m, indexNs=self.indexNs, timeAndLocation=timeAndLocation, currentState=initialState)
        
        transitionOutput : TransitionOutput = transitionGenerator.insideLayerOperations(
            currentRayState=initialState)

        self.assertEqual(transitionOutput.interface.newAltitude_m, 0.0)
        self.assertEqual(transitionOutput.interface.n_2, 3.0)

    def test_insideLayerOperations_across(self):
        # initial structure
        initialElevationAngle_deg = -2.0
        initialLLA = LLA_Coord(0.0, 0.0, 9000.0)
        initialNIndex = 0.95

        initialState = RayState(exitElevation_deg=initialElevationAngle_deg, exitAzimuth_deg=self.initialAzimuth_deg,
                                lla=initialLLA)

        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=initialLLA, eventTime_UTC=currentDateTime
        )

        transitionGenerator = TransitionGenerator(
            heights_m=self.heights_m, indexNs=self.indexNs, timeAndLocation=timeAndLocation, currentState=initialState)
        
        transitionOutput : TransitionOutput = transitionGenerator.insideLayerOperations(
            currentRayState=initialState)

        self.assertEqual(transitionOutput.interface.newAltitude_m, 10000)
        self.assertEqual(transitionOutput.interface.n_2, 0.95)

    def test_insideLayerOperations_acrossSame(self):

        # initial structure
        initialElevationAngle_deg = -2.0
        initialLLA = LLA_Coord(0.0, 0.0, 10000.0)
        initialNIndex = 0.95

        initialState = RayState(exitElevation_deg=initialElevationAngle_deg, exitAzimuth_deg=self.initialAzimuth_deg,
                                lla=initialLLA)

        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=initialLLA, eventTime_UTC=currentDateTime
        )

        transitionGenerator = TransitionGenerator(
            heights_m=self.heights_m, indexNs=self.indexNs, timeAndLocation=timeAndLocation, currentState=initialState)
        
        transitionOutput : TransitionOutput = transitionGenerator.insideLayerOperations(
            currentRayState=initialState)

        self.assertEqual(transitionOutput.interface.newAltitude_m, 10000)
        self.assertEqual(transitionOutput.interface.n_2, 0.95)

    def test_onTheEdgeOperations_up(self):
        # initial structure
        initialElevationAngle_deg = 89.0
        initialLLA = LLA_Coord(0.0, 0.0, 0.0)
        initialNIndex = 1.0

        initialState = RayState(exitElevation_deg=initialElevationAngle_deg, exitAzimuth_deg=self.initialAzimuth_deg,
                                lla=initialLLA)

        layerOutput = Interface(n_1=1.0, n_2=1.0, entryAngle_deg=0.0,
                                newAltitude_m=100, intersection_LLA=LLA_Coord(0.0, 0.0, 100.0))

        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=initialLLA, eventTime_UTC=currentDateTime
        )
        transitionGenerator = TransitionGenerator(
            heights_m=self.heights_m, indexNs=self.indexNs, timeAndLocation=timeAndLocation, currentState=initialState)

        currentState = transitionGenerator.onTheEdgeOperations(
            currentState=initialState, interface=layerOutput)

        self.assertEqual(currentState.lla.altitude_m, 100.0)
        self.assertEqual(currentState.exitElevation_deg, 90.0)

    def test_onTheEdgeOperations_down(self):
        # initial structure
        initialElevationAngle_deg = -89.0
        initialLLA = LLA_Coord(lat_deg= 0.0, lon_deg = 0.0, altitude_m = 1000.0)
        initialNIndex = 1.0

        initialState = RayState(exitElevation_deg=initialElevationAngle_deg, exitAzimuth_deg=self.initialAzimuth_deg,
                                lla=initialLLA)

        layerOutput = Interface(
            1.0, 1.0, -1.0,  100.0, LLA_Coord(0.0, 0.0, 100.0))

        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=initialLLA, eventTime_UTC=currentDateTime
        )
        transitionGenerator = TransitionGenerator(
            heights_m=self.heights_m, indexNs=self.indexNs, timeAndLocation=timeAndLocation, currentState=initialState)

        currentState = transitionGenerator.onTheEdgeOperations(
            currentState=initialState, interface=layerOutput)

        self.assertEqual(currentState.lla.altitude_m, 100.0)
        self.assertTrue(currentState.exitElevation_deg < -87.0)

    def test_onTheEdgeOperations_bounce(self):
        # initial structure
        initialElevationAngle_deg = -89.0
        initialLLA = LLA_Coord(0.0, 0.0, 100.0)
        initialNIndex = 1.0

        initialState = RayState(exitElevation_deg=initialElevationAngle_deg, exitAzimuth_deg=self.initialAzimuth_deg,
                                lla=initialLLA)

        layerOutput = Interface(
            1.0, 3.0, -1.0,  0.0, LLA_Coord(0.0, 0.0, 0.0))

        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=initialLLA, eventTime_UTC=currentDateTime
        )
        transitionGenerator = TransitionGenerator(
            heights_m=self.heights_m, indexNs=self.indexNs, timeAndLocation=timeAndLocation, currentState=initialState)

        currentState = transitionGenerator.onTheEdgeOperations(
            currentState=initialState, interface=layerOutput)

        self.assertEqual(currentState.lla.altitude_m, 0.0)
        self.assertTrue(currentState.exitElevation_deg > 87.0)

    # ============================================================

    def test_raytracer_reflect(self):
        indexNs = [1.0, 0.95, 0.85, 0.55, 0.97, 1.0]

        # initial structure
        initialElevationAngle_deg = 45.0
        initialLLA = LLA_Coord(0.0, 0.0, 0.0)

        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=initialLLA, eventTime_UTC=currentDateTime
        )
        rayTracer = RayTracer(
            heights_m=self.heights_m, indexNs=indexNs, timeAndLocation=timeAndLocation)

        stateList = rayTracer.execute(
            params=[self.initialAzimuth_deg, initialElevationAngle_deg])
  
        self.assertTrue(len(stateList) == 59)


if __name__ == '__main__':
    unittest.main()
