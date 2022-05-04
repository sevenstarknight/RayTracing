from rdp import rdp
import numpy as np
from scipy import interpolate
from scipy import optimize

import logging

# ====================================================
# local
from src.stratification.abstractquantizer import AbstractQuantizer
from src.stratification.quantization_class import Quantization
from src.stratification.quantizationparameter_class import QuantizationParameter
from stratification.twodseries_class import TwoDSeries

# ====================================================
# constants
MAXITER = 100000
LOGGER = logging.getLogger("mylogger")

class RDPQuantizer(AbstractQuantizer):

    def generateQuantization(self, quantizationParameter : QuantizationParameter) -> Quantization: 
        if(quantizationParameter.epsilon is None):
            raise Exception("quantizationParameter.epsilon, can't be none")
            
        epsilon = quantizationParameter.epsilon

        objectivefunction = self.ObjectiveFunction(self)

        twoDSeries = objectivefunction.generateTwoDSeries(epsilon)

        return(Quantization(twoDSeries.x_inputSeries, twoDSeries.y_inputSeries))


    def generateOptimalQuantization(self) -> Quantization:
        objectivefunction = self.ObjectiveFunction(self)

        minimum = optimize.brent(lambda x: objectivefunction.estimate(x),brack=(-6,0,6))

        twoDSeries = objectivefunction.generateTwoDSeries(minimum)
        return(Quantization(twoDSeries.x_inputSeries, twoDSeries.y_inputSeries))
        

    class ObjectiveFunction():
        def __init__(self, outer:'RDPQuantizer'):
            self.data = outer.inputSeries.getMatrix
            self.inputSeries = outer.inputSeries
        
        def generateTwoDSeries(self, log_x:float) -> TwoDSeries:
            mask = rdp(self.data, epsilon = 10^log_x, algo="iter", return_mask=True)
            maskedData = self.data[mask]
            splitData = np.hsplit(maskedData, 2)
            xAxis = np.transpose(splitData[0])
            yAxis = np.transpose(splitData[1])

            return(TwoDSeries(x_inputSeries=xAxis, y_inputSeries=yAxis))


        def estimate(self, log_x:float) -> float:

            twoDSeries = self.generateTwoDSeries(xAxis, yAxis)

            fStar = interpolate.InterpolatedUnivariateSpline(xAxis, yAxis)

            rss = 0
            for idx in range(len(self.inputSeries.x_inputSeries)):
                x = self.inputSeries.x_inputSeries[idx]
                y = self.inputSeries.y_inputSeries[idx]
                yStar = fStar(x)

                rss += (y - yStar)*(y - yStar)

            t = len(self.inputSeries.x_inputSeries)
            k = len(xAxis)
            bic = t*np.log(rss/t) + k*np.log(t)

            return(bic)