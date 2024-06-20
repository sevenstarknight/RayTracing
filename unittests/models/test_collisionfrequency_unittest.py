# STDLIB modules
import unittest
from datetime import datetime

# FIRSTPARTY modules
from src.bindings.positional.layer_class import Layer
from src.bindings.models.ionospherestate_class import IonosphereState
from src.models.collisionfrequency import ElectronIonCollisionFrequency, ElectronNeutralCollisionFrequency
from src.models.iri_model import IRI_Model
from src.models.msise_model import MSISE_Model
from unittests.testutilities import TestUtilities


class TestCollisionFrequency(unittest.TestCase):

    def test_ElectronIonCollisionFrequency(self):
        ap = [1, 2, 3, 4, 2, 2, 1]
        ionosphereState = IonosphereState(20.5, 20.6, ap)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)

        iriModel = IRI_Model(ionosphereState=ionosphereState,
                             currentDateTime=currentDateTime)

        collisionFrequency = ElectronIonCollisionFrequency()

        slantLayers : list[Layer] = TestUtilities.generateSlantPath()

        iriOutputs = iriModel.generateSetEstimate(layers=slantLayers)

        vei = collisionFrequency.estimateCollisionFreq(iriOutput=iriOutputs[4])

        self.assertTrue(vei > 0)

    def test_ElectronNeutralCollisionFrequency(self):
        ap = [1, 2, 3, 4, 2, 2, 1]
        ionosphereState = IonosphereState(20.5, 20.6, ap)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)

        iriModel = IRI_Model(ionosphereState=ionosphereState,
                             currentDateTime=currentDateTime)
        msiseModel = MSISE_Model(
            ionosphereState=ionosphereState, currentDateTime=currentDateTime)

        collisionFrequency = ElectronNeutralCollisionFrequency()

        slantLayers : list[Layer] =  TestUtilities.generateSlantPath()

        iriOutputs = iriModel.generateSetEstimate(layers=slantLayers)
        msiseOutputs = msiseModel.generateSetEstimate(layers=slantLayers)

        ven = collisionFrequency.estimateCollisionFreq(
            iriOutput=iriOutputs[4], msiseOutput=msiseOutputs[4])

        self.assertTrue(ven > 0)


if __name__ == '__main__':
    unittest.main()
