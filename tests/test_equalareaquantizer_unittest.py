import unittest

import numpy as np

from src.stratification.equalareaquantizer import EqualAreaQuantizer
from src.stratification.twodseries_class import TwoDSeries



class TestCoordinates(unittest.TestCase):

    def test_GenerateQuantization(self):

        cycles = 2 # how many sine cycles
        resolution = 1125 # how many datapoints to generate

        length = np.pi * 2 * cycles
        my_wave = np.fabs(np.sin(np.arange(0, length, length / resolution)))

        samples = np.linspace(0, len(my_wave), len(my_wave), endpoint=False)

        testSeries = TwoDSeries(samples, my_wave)

        eaq = EqualAreaQuantizer(testSeries)

        quantization = eaq.generateQuantization(100)

        self.assertIsNotNone(quantization)


if __name__ == '__main__':
    unittest.main()