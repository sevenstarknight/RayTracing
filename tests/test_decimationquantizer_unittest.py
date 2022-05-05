import unittest

import numpy as np
import scipy.io
# ====================================================
# local imports
from src.stratification.decimationquantizer import DecimationQuantizer
from src.stratification.twodseries_class import TwoDSeries
from src.stratification.quantizationparameter_class import QuantizationParameter
from stratification.stratificationmethod_enum import StratificationMethod

class TestDecimationQuantizer(unittest.TestCase):
    def setUp(self) -> None:
        self.mat = scipy.io.loadmat('tests/data/QuantizerDataTest.mat')

    def test_GenerateQuantization_EDP(self):
        xAxis = np.transpose(np.array(self.mat['alt']))[0]
        yAxis = np.transpose(np.array(self.mat['EDP']))[0]

        testSeries = TwoDSeries(xAxis, yAxis)

        quantizer = DecimationQuantizer(testSeries)

        quantizationParameter = QuantizationParameter(StratificationMethod.DECIMATION_MODEL,nQuant=10)

        quantization = quantizer.generateQuantization(quantizationParameter)

        self.assertIsNotNone(quantization)

    def test_GenerateQuantization(self):

        cycles = 2 # how many sine cycles
        resolution = 1125 # how many datapoints to generate

        length = np.pi * 2 * cycles
        my_wave = np.fabs(np.sin(np.arange(0, length, length / resolution)))

        samples = np.linspace(0, len(my_wave), len(my_wave), endpoint=False)

        testSeries = TwoDSeries(samples, my_wave)

        quantizer = DecimationQuantizer(testSeries)

        quantizationParameter = QuantizationParameter(StratificationMethod.DECIMATION_MODEL,nQuant=10)

        quantization = quantizer.generateQuantization(quantizationParameter)

        self.assertIsNotNone(quantization)


if __name__ == '__main__':
    unittest.main()