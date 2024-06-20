# STDLIB modules
import unittest
from datetime import datetime

# FIRSTPARTY modules
from src.bindings.positional.satelliteinformation_class import SatelliteInformation
from src.positional.satellitepositiongenerator import SatellitePositionGenerator


class TestCoordinates(unittest.TestCase):

    def test_SatPosGenerator(self):

        s = '1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991'
        t = '2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482'
        name = "Test"

        satelliteInformation = SatelliteInformation(name=name, s=s, t=t)

        satPosGenerator = SatellitePositionGenerator(satelliteInformation)

        dateTime = datetime(2012, 9, 15, 13, 14, 30)

        testECEF = satPosGenerator.estimatePosition_ECEF(dateTime)

        self.assertTrue(testECEF.magnitude() > 0.0)


if __name__ == '__main__':
    unittest.main()
