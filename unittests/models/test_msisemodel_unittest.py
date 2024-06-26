# STDLIB modules
import unittest
from datetime import datetime

# FIRSTPARTY modules
from src.bindings.positional.layer_class import Layer
from src.bindings.models.ionospherestate_class import IonosphereState
from src.models.msise_model import MSISE_Model
from unittests.testutilities import TestUtilities

class TestMSISE_Model(unittest.TestCase):

    def test_msiseModel(self):

        ap = [1, 2, 3, 4, 2, 2, 1]
        ionosphereState = IonosphereState(20.5, 20.6, ap)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)

        msiseModel = MSISE_Model(
            ionosphereState=ionosphereState, currentDateTime=currentDateTime)

        slantLayers : list[Layer] =  TestUtilities.generateSlantPath()

        msiseOutputs = msiseModel.generateSetEstimate(layers=slantLayers)

        self.assertTrue(len(msiseOutputs) > 0)


if __name__ == '__main__':
    unittest.main()
