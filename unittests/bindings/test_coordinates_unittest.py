import unittest
import ahrs

# FIRSTPARTY modules
from src.bindings.positional.coordinates_class import LLA_Coord, ECEF_Coord


class TestCoordinates(unittest.TestCase):

    def test_LLA(self):
        testLLA = LLA_Coord(0.0, 0.0, 0.0)

        self.assertEqual(testLLA.lat_deg, 0.0)

    def test_ECEF(self):
        wgs = ahrs.utils.WGS()

        testECEF = ECEF_Coord(wgs.a, 0.0, 0.0)
        self.assertEqual(testECEF.x_m, wgs.a)

        deltaECEF = ECEF_Coord.subtract(testECEF, testECEF)
        self.assertEqual(deltaECEF.x_m, 0.0)

        magECEF = testECEF.magnitude()
        self.assertEqual(magECEF, wgs.a)


if __name__ == '__main__':
    unittest.main()
