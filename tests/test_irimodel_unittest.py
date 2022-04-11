import unittest
from datetime import datetime
# https://pyproj4.github.io/pyproj/stable/
import pyproj

from supportTestStructures import generateSlantPath

# ====================================================
# local imports
from raytracing.bindings.ionospherestate_class import IonosphereState
from raytracing.models.iri_model import IRI_Model

ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


class TestIRIModel(unittest.TestCase):

    def test_iriModel(self):

        ap = [1, 2, 3, 4, 2, 2, 1]
        ionosphereState = IonosphereState(20.5, 20.6, ap)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)

        iriModel = IRI_Model(ionosphereState=ionosphereState,
                             currentDateTime=currentDateTime)

        slantPath = generateSlantPath()

        iriOutputs = iriModel.generateSetEstimateFromRayState(
            rayPoints=slantPath)

        self.assertTrue(len(iriOutputs) > 0)


if __name__ == '__main__':
    unittest.main()
