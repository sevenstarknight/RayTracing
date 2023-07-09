import unittest

# ====================================================
# local imports
from src.bindings.models.ionospherestate_class import IonosphereState
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.raypatheffects import EstimateRayPathEffects
from src.stratification.quantizationparameter_class import QuantizationParameter
from src.stratification.stratificationmethod_enum import StratificationMethod
from tests.unittest_computations import standardSatelliteInformation, standardStartingPoint


class TestRayPathEffects(unittest.TestCase):

    def test_RayPathEffects(self):

        ap = [1, 2, 3, 4, 2, 2, 1]
        ionosphereState = IonosphereState(20.5, 20.6, ap)

        satelliteInformation = standardSatelliteInformation()

        timeAndLocation = standardStartingPoint(satelliteInformation)
        
        # ======================================================
        optimizer = EstimateRayPathEffects(
            timeAndLocation=timeAndLocation, dispersionModel=DispersionModel.X_MODEL, 
            transportMode=TransportMode.PLASMA_MODE)
        freq_Hz = 1000e6
        
        quantizationParameter = QuantizationParameter(StratificationMethod.DECIMATION_MODEL,nQuant=10)

        transIonosphereEffects = optimizer.estimate(
            freq_Hz=freq_Hz, satelliteInformation=satelliteInformation, ionosphereState=ionosphereState,
             quantizationParameter = quantizationParameter)

        self.assertTrue(transIonosphereEffects is not None)


if __name__ == '__main__':
    unittest.main()
