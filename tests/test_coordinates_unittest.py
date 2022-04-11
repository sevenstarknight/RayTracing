import unittest
import ahrs

# ====================================================
# local imports
from src.bindings import coordinates_class


class TestCoordinates(unittest.TestCase):

    def test_LLA(self):
        testLLA = coordinates_class.LLA(0.0, 0.0, 0.0)

        self.assertEqual(testLLA.lat_deg, 0.0)

    def test_ECEF(self):
        wgs = ahrs.utils.WGS()

        testECEF = coordinates_class.ECEF(wgs.a, 0.0, 0.0)
        self.assertEqual(testECEF.x_m, wgs.a)

        deltaECEF = coordinates_class.ECEF.subtract(testECEF, testECEF)
        self.assertEqual(deltaECEF.x_m, 0.0)

        magECEF = testECEF.magnitude()
        self.assertEqual(magECEF, wgs.a)


if __name__ == '__main__':
    unittest.main()
