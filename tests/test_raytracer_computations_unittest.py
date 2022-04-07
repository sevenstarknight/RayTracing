import unittest
import math
import ahrs
import pyproj

from raytracing import raytracer
from raytracing.bindings import coordinates_class

class TestRayTracer_Computations(unittest.TestCase):

    def test_computeGeocentricRadius(self):
        initialLLA = coordinates_class.LLA(0.0, 345.5975, 0.0)
        radius = raytracer.computeGeocentricRadius(initialLLA)
        wgs = ahrs.utils.WGS()
        self.assertTrue(math.fabs(wgs.a- radius) < 0.1)

    def test_computeNewIntersection(self):
        wgs = ahrs.utils.WGS()
        initialECEF = coordinates_class.ECEF(wgs.a, 0.0, 0.0)
        initialECEF_vector = coordinates_class.ECEF(1.0, 0.0, 0.0)
        newAltitude_m = 100.0

        intersectionECEF = raytracer.computeNewIntersection(initialECEF, initialECEF_vector, newAltitude_m)

        delta = coordinates_class.ECEF.subtract(initialECEF, intersectionECEF)
        self.assertTrue(math.fabs(newAltitude_m - delta.magnitude()) < 0.1)

    def test_computeEntryAngle(self):
        wgs = ahrs.utils.WGS()
        initialECEF_1 = coordinates_class.ECEF(wgs.a, 0.0, 0.0)
        initialECEF_2 = coordinates_class.ECEF(wgs.a + 100.0, 10.0, 0.0)

        ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
        lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')

        lat_deg, lon_deg, alt_m = pyproj.transform(ecef, lla, initialECEF_1.x_m, initialECEF_1.y_m, initialECEF_1.z_m, radians=False)
        lla_p1 = coordinates_class.LLA(lat_deg, lon_deg, alt_m)

        lat_deg, lon_deg, alt_m = pyproj.transform(ecef, lla, initialECEF_2.x_m, initialECEF_2.y_m, initialECEF_2.z_m, radians=False)
        lla_p2 = coordinates_class.LLA(lat_deg, lon_deg, alt_m)

        entryAngle = raytracer.computeEntryAngle(90.0, initialECEF_1, initialECEF_2, lla_p1, lla_p2)

        self.assertTrue(math.fabs(5.7015 - entryAngle) < 0.1)
