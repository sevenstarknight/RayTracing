import numpy as np
import pandas as pd
import math
from tqdm import trange, tqdm
import unittest

import sys
sys.path.append("../")
# ======================================================================================
# Local imports
from src.endtoenddemonstration import EndToEndDemo
from src.stratification.quantizationparameter_class import QuantizationParameter
from src.stratification.stratificationmethod_enum import StratificationMethod

class TestDecimation(unittest.TestCase):

    def test_Decimation(self):

        end2EndDemo = EndToEndDemo()

        results_eqa = pd.DataFrame()
        #iterRange = np.arange(0,4,0.1)
        iterRange = np.arange(3.6,4,0.1)
        listOfResults_eqa = []

        for idx in tqdm(iterRange):
            nQuant = math.ceil(10**idx)
            quantizationParameter = QuantizationParameter(StratificationMethod.EQUALAREA_MODEL,nQuant=nQuant)
            transIonosphereEffects = end2EndDemo.execute_X(quantizationParameter)
            result = {}
            result["nQuant"] = nQuant
            result["layers"] = len(transIonosphereEffects.rayStates)
            result["totalIonoDelay_sec"] = transIonosphereEffects.totalIonoDelay_sec
            result["totalIonoLoss_db"] = transIonosphereEffects.totalIonoLoss_db
            result["totalGeoDistance_m"] = transIonosphereEffects.totalGeoDistance_m

            listOfResults_eqa.append(result)