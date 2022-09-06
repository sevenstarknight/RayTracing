import unittest
from datetime import datetime

# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj

# ====================================================
# local imports
from src.bindings.positional.coordinates_class import LLA_Coord
from src.bindings.models.ionospherestate_class import IonosphereState
from src.bindings.positional.satelliteinformation_class import SatelliteInformation
from src.bindings.positional.timeandlocation_class import TimeAndLocation
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.positional.satellitepositiongenerator import SatellitePositionGenerator
from src.stratification.quantizationparameter_class import QuantizationParameter
from src.stratification.stratificationmethod_enum import StratificationMethod
from src.stratification.stratificationoptimizer import StratificationOptimizer
from tests.unittest_computations import standardSatelliteInformation, standardStartingPoint

# ====================================================
# constants
ECEF = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
LLA = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


class TestStratificationOptimizer(unittest.TestCase):

    def test_StratificationOptimizer(self):

        ionosphereState = IonosphereState(10.0, 10.0, 3.0)

        satelliteInformation = standardSatelliteInformation()

        timeAndLocation = standardStartingPoint(satelliteInformation)
        # ======================================================

        stratificationOptimizer = StratificationOptimizer(dispersionModel=DispersionModel.X_MODEL, 
        timeAndLocation=timeAndLocation, transportMode=TransportMode.PLASMA_MODE)

        quantizationParameter = QuantizationParameter(StratificationMethod.DECIMATION_MODEL,nQuant=10)

        heights_m = stratificationOptimizer.generateHeightModel(freq_Hz=10e6, quantizationParameter=quantizationParameter,
        ionosphereState=ionosphereState,satelliteInformation=satelliteInformation)
        
        self.assertTrue(heights_m is not None)


if __name__ == '__main__':
    unittest.main()
