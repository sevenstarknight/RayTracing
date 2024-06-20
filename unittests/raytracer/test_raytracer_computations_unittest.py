import unittest
import math

# ====================================================
# https://ahrs.readthedocs.io/en/latest/
import ahrs
# ====================================================
# local imports
from src.positional.locationconverter_computations import LocationConverterComputation
from src.raytracer.raytracer import RayTracerComputations
from src.bindings.positional.coordinates_class import ECEF_Coord, LLA_Coord



class TestRayTracer_Computations(unittest.TestCase):

    def test_computeGeocentricRadius(self):
        initialLLA = LLA_Coord(0.0, 345.5975, 0.0)
        radius = RayTracerComputations.computeGeocentricRadius(initialLLA)
        wgs = ahrs.utils.WGS()
        self.assertTrue(math.fabs(wgs.a - radius) < 0.1)

    def test_computeNewIntersection(self):
        wgs = ahrs.utils.WGS()
        initialECEF = ECEF_Coord(wgs.a, 0.0, 0.0)
        initialECEF_vector = ECEF_Coord(1.0, 0.0, 0.0)
        newAltitude_m = 100.0

        intersectionECEF = RayTracerComputations.computeNewIntersection(
            initialECEF, initialECEF_vector, newAltitude_m)

        delta = ECEF_Coord.subtract(initialECEF, intersectionECEF)
        self.assertTrue(math.fabs(newAltitude_m - delta.magnitude()) < 0.1)

    def test_computeEntryAngle(self):
        wgs = ahrs.utils.WGS()
        initialECEF_1 = ECEF_Coord(wgs.a, 0.0, 0.0)
        initialECEF_2 = ECEF_Coord(wgs.a + 100.0, 10.0, 0.0)


        lla_p1: LLA_Coord = LocationConverterComputation.convertFromECEFtoLLA(ecef=initialECEF_1)

        lla_p2: LLA_Coord = LocationConverterComputation.convertFromECEFtoLLA(ecef=initialECEF_2)

        entryAngle = RayTracerComputations.computeEntryAngle(
            90.0, initialECEF_1, initialECEF_2, lla_p1, lla_p2)

        self.assertTrue(math.fabs(5.7015 - entryAngle) < 0.1)
