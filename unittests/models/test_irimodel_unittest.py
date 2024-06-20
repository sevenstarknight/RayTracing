import unittest
from datetime import datetime

# FIRSTPARTY modules
from src.bindings.positional.layer_class import Layer
from supportTestStructures import generateSlantPath
from src.bindings.models.ionospherestate_class import IonosphereState
from src.models.iri_model import IRI_Model


class TestIRIModel(unittest.TestCase):

    def test_iriModel(self):

        ap = [1, 2, 3, 4, 2, 2, 1]
        ionosphereState = IonosphereState(20.5, 20.6, ap)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)

        iriModel = IRI_Model(ionosphereState=ionosphereState,
                             currentDateTime=currentDateTime)

        slantLayers : list[Layer] =  generateSlantPath()

        iriOutputs = iriModel.generateSetEstimate(layers=slantLayers)

        self.assertTrue(len(iriOutputs) > 0)


if __name__ == '__main__':
    unittest.main()
