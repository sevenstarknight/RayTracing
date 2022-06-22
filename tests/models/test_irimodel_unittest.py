import unittest
from datetime import datetime

# ====================================================
# local imports
from supportTestStructures import generateSlantPath

from src.bindings.ionospherestate_class import IonosphereState
from src.models.iri_model import IRI_Model


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
