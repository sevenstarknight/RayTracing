# STDLIB modules
import unittest
import math

# THIRDPARTY modules
import numpy as np
import pandas as pd
from tqdm import tqdm

# FIRSTPARTY modules
from src.endtoenddemonstration import EndToEndDemo
from src.stratification.quantizationparameter_class import QuantizationParameter
from src.stratification.stratificationmethod_enum import StratificationMethod

class TestDemoDecimation(unittest.TestCase):

    def test_DemoDecimation_X(self):

        end2EndDemo = EndToEndDemo()

        iterRange = np.arange(1.0,2.0,0.2)
        listOfResults_eqa = []

        for idx in tqdm(iterRange):
            nQuant = math.ceil(10**idx)
            quantizationParameter = QuantizationParameter(StratificationMethod.EQUALAREA_MODEL,nQuant=nQuant)
            transIonosphereEffects = end2EndDemo.execute_X(quantizationParameter)
            result = {}
            result["nQuant"] = nQuant
            result["layers"] = len(transIonosphereEffects.rayVectors)
            result["totalIonoDelay_sec"] = transIonosphereEffects.totalIonoDelay_sec
            result["totalIonoLoss_db"] = transIonosphereEffects.totalIonoLoss_db
            result["totalGeoDistance_m"] = transIonosphereEffects.totalGeoDistance_m

            listOfResults_eqa.append(result)

        listOfResults_eqa_df = pd.DataFrame(listOfResults_eqa)


        print(listOfResults_eqa_df.to_markdown())


    def test_DemoDecimation_XY(self):

        end2EndDemo = EndToEndDemo()

        iterRange = np.arange(1.0,2.0,0.2)
        listOfResults_eqa = []

        for idx in tqdm(iterRange):
            nQuant = math.ceil(10**idx)
            quantizationParameter = QuantizationParameter(StratificationMethod.EQUALAREA_MODEL,nQuant=nQuant)
            transIonosphereEffects = end2EndDemo.execute_XY(quantizationParameter)
            result = {}
            result["nQuant"] = nQuant
            result["layers"] = len(transIonosphereEffects.rayVectors)
            result["totalIonoDelay_sec"] = transIonosphereEffects.totalIonoDelay_sec
            result["totalIonoLoss_db"] = transIonosphereEffects.totalIonoLoss_db
            result["totalGeoDistance_m"] = transIonosphereEffects.totalGeoDistance_m

            listOfResults_eqa.append(result)

        listOfResults_eqa_df = pd.DataFrame(listOfResults_eqa)


        print(listOfResults_eqa_df.to_markdown())