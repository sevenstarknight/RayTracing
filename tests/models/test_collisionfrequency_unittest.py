import unittest
from datetime import datetime

# ====================================================
# local imports
from supportTestStructures import generateSlantPath

from src.bindings.models.ionospherestate_class import IonosphereState
from src.models.collisionfrequency import ElectronIonCollisionFrequency, ElectronNeutralCollisionFrequency
from src.models.iri_model import IRI_Model
from src.models.msise_model import MSISE_Model


class TestCollisionFrequency(unittest.TestCase):

    def test_ElectronIonCollisionFrequency(self):
        ap = [1, 2, 3, 4, 2, 2, 1]
        ionosphereState = IonosphereState(20.5, 20.6, ap)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)

        iriModel = IRI_Model(ionosphereState=ionosphereState,
                             currentDateTime=currentDateTime)

        collisionFrequency = ElectronIonCollisionFrequency()

        slantPath = generateSlantPath()

        iriOutputs = iriModel.generateSetEstimateFromRayState(
            rayPoints=slantPath)

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

        slantPath = generateSlantPath()

        iriOutputs = iriModel.generateSetEstimateFromRayState(
            rayPoints=slantPath)
        msiseOutputs = msiseModel.generateSetEstimateFromRayState(
            rayPoints=slantPath)

        ven = collisionFrequency.estimateCollisionFreq(
            iriOutput=iriOutputs[4], msiseOutput=msiseOutputs[4])

        self.assertTrue(ven > 0)


if __name__ == '__main__':
    unittest.main()
