# STDLIB modules
import unittest

# THIRDPARTY modules
import pandas as pd

# FIRSTPARTY modules
from src.bindings.models.ionospherestate_class import IonosphereState
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.stratification.quantizationparameter_class import QuantizationParameter
from src.stratification.stratificationmethod_enum import StratificationMethod
from src.raypatheffects import EstimateRayPathEffects
from unittests.testutilities import TestUtilities


class TestStratificationIntegration(unittest.TestCase):

    def test_StratificationOptimizer(self):

        satelliteInformation = TestUtilities.standardSatelliteInformation()

        timeAndLocation = TestUtilities.standardStartingPoint(satelliteInformation)

        ionosphereState = IonosphereState(150.0, 150.0, 3.0)

        # ======================================================
        estimateRayPathEffects = EstimateRayPathEffects(
            timeAndLocation=timeAndLocation, dispersionModel=DispersionModel.X_MODEL,
            transportMode=TransportMode.PLASMA_MODE)

        freq_Hz = 1000*6

        quantizationParameter = QuantizationParameter(
            StratificationMethod.DECIMATION_MODEL, nQuant=20)

        transIonosphereEffects = estimateRayPathEffects.estimate(freq_Hz=freq_Hz,
                                                                 quantizationParameter=quantizationParameter,
                                                                 ionosphereState=ionosphereState, satelliteInformation=satelliteInformation)

        print(transIonosphereEffects.totalIonoDelay_sec)
        print(transIonosphereEffects.totalIonoLoss_db)

        rayVectors = transIonosphereEffects.rayVectors
        listTmp = []
        columnNames = []
        for rayVector in rayVectors:
            tmpList = rayVector.rayState.generateList()
            listTmp.append(tmpList)
            columnNames = rayVector.rayState.generateColumnNames()

        df = pd.DataFrame(listTmp, columns=columnNames, dtype=float)
