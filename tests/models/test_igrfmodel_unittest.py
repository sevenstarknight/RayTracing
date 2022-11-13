import unittest
from datetime import datetime
from src.bindings.positional.layer_class import Layer
# ====================================================
# local imports
from supportTestStructures import generateSlantPath

from src.bindings.models.ionospherestate_class import IonosphereState
from src.models.igrf_model import IGRF_Model


class TestIGRFModel(unittest.TestCase):

    def test_igrfModel(self):

        ap = [1, 2, 3, 4, 2, 2, 1]
        ionosphereState = IonosphereState(20.5, 20.6, ap)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)

        igrfModel = IGRF_Model(
            ionosphereState=ionosphereState, currentDateTime=currentDateTime)

        slantLayers : list[Layer] =  generateSlantPath()

        igrfOutputs = igrfModel.generateSetEstimate(layers=slantLayers)

        self.assertTrue(len(igrfOutputs) > 0)


if __name__ == '__main__':
    unittest.main()
