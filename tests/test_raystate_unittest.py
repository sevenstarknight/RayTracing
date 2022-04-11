import unittest

# ====================================================
# local imports
from raytracing import raystate_class
from raytracing.bindings import coordinates_class


class TestRayState(unittest.TestCase):

    def test_raystate(self):
        exitElevation_deg = 0.0
        exitAzimuth_deg = 0.0
        lla = coordinates_class.LLA(0.0, 0.0, 0.0)
        nIndex = complex(1.0, 0.0)
        rayState1 = raystate_class.RayState(
            exitElevation_deg, exitAzimuth_deg, lla, nIndex)

        self.assertEqual(rayState1.exitAzimuth_deg, exitAzimuth_deg)


if __name__ == '__main__':
    unittest.main()
