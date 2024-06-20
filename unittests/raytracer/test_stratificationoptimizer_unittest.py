# STDLIB modules
import unittest

# FIRSTPARTY modules
from src.bindings.models.ionospherestate_class import IonosphereState
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.stratification.quantizationparameter_class import QuantizationParameter
from src.stratification.stratificationmethod_enum import StratificationMethod
from src.raytracer.stratificationoptimizer import StratificationOptimizer
from unittests.testutilities import TestUtilities


class TestStratificationOptimizer(unittest.TestCase):

    def test_StratificationOptimizer(self):

        ionosphereState = IonosphereState(10.0, 10.0, 3.0)

        satelliteInformation = TestUtilities.standardSatelliteInformation()

        timeAndLocation = TestUtilities.standardStartingPoint(satelliteInformation)
        # ======================================================

        stratificationOptimizer = StratificationOptimizer(dispersionModel=DispersionModel.X_MODEL, 
        timeAndLocation=timeAndLocation, transportMode=TransportMode.PLASMA_MODE)

        quantizationParameter = QuantizationParameter(StratificationMethod.DECIMATION_MODEL,nQuant=10)

        heights_m = stratificationOptimizer.generateHeightModel(freq_Hz=10e6, quantizationParameter=quantizationParameter,
        ionosphereState=ionosphereState,satelliteInformation=satelliteInformation)
        
        self.assertTrue(heights_m is not None)


if __name__ == '__main__':
    unittest.main()
