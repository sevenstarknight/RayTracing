import unittest
from datetime import datetime

# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj

# ====================================================
# local imports
from supportTestStructures import generateSlantPath

from src.bindings.ionospherestate_class import IonosphereState
from src.models.igrf_model import IGRF_Model

# ====================================================
# constants
ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


class TestIGRFModel(unittest.TestCase):

    def test_igrfModel(self):

        ap = [1, 2, 3, 4, 2, 2, 1]
        ionosphereState = IonosphereState(20.5, 20.6, ap)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)

        igrfModel = IGRF_Model(
            ionosphereState=ionosphereState, currentDateTime=currentDateTime)

        slantPath = generateSlantPath()

        igrfOutputs = igrfModel.generateSetEstimateFromRayState(
            rayPoints=slantPath)

        self.assertTrue(len(igrfOutputs) > 0)


if __name__ == '__main__':
    unittest.main()
