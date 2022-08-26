import unittest

# ====================================================
# local imports
from src.raystate_class import RayState
from src.bindings.positional.coordinates_class import LLA_Coord

class TestRayState(unittest.TestCase):

    def test_raystate(self):
        exitElevation_deg = 0.0
        exitAzimuth_deg = 0.0
        lla = LLA_Coord(0.0, 0.0, 0.0)
        nIndex = complex(1.0, 0.0)
        rayState1 = RayState(
            exitElevation_deg, exitAzimuth_deg, lla, nIndex)

        self.assertEqual(rayState1.exitAzimuth_deg, exitAzimuth_deg)


if __name__ == '__main__':
    unittest.main()
