import unittest

import numpy as np
import scipy.io
# ====================================================
# local imports
from src.stratification.lloydmaxquantizer import LloydMaxQuantizer
from src.stratification.twodseries_class import TwoDSeries



class TestLloydMaxQuantizer(unittest.TestCase):
    def setUp(self) -> None:
        self.mat = scipy.io.loadmat('tests/data/QuantizerDataTest.mat')

    def test_GenerateQuantization_EDP(self):
        xAxis = np.transpose(np.array(self.mat['alt']))[0]
        yAxis = np.transpose(np.array(self.mat['EDP']))[0]

        testSeries = TwoDSeries(xAxis, yAxis)

        quantizer = LloydMaxQuantizer(testSeries)

        quantization = quantizer.generateQuantization(180)

        self.assertIsNotNone(quantization)

    def test_GenerateQuantization(self):

        cycles = 2 # how many sine cycles
        resolution = 1125 # how many datapoints to generate

        length = np.pi * 2 * cycles
        my_wave = np.fabs(np.sin(np.arange(0, length, length / resolution)))

        samples = np.linspace(0, len(my_wave), len(my_wave), endpoint=False)

        testSeries = TwoDSeries(samples, my_wave)

        quantizer = LloydMaxQuantizer(testSeries)

        quantization = quantizer.generateQuantization(100)

        self.assertIsNotNone(quantization)


if __name__ == '__main__':
    unittest.main()