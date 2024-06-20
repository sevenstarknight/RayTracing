# THIRDPARTY modules
from rdp import rdp
import numpy as np
from scipy import interpolate
from scipy import optimize
# FIRSTPARTY modules
from src.stratification.abstractquantizer import AbstractQuantizer
from src.stratification.quantization_class import Quantization
from src.stratification.quantizationparameter_class import QuantizationParameter
from src.stratification.twodseries_class import TwoDSeries

# ====================================================
# constants
MAXITER = 100000


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

        minimum = optimize.brent(lambda x: objectivefunction.estimate(x),brack=(-6,0))

        twoDSeries = objectivefunction.generateTwoDSeries(minimum)
        return(Quantization(twoDSeries.x_inputSeries, twoDSeries.y_inputSeries))
        

    class ObjectiveFunction():
        def __init__(self, outer:'RDPQuantizer'):
            self.inputSeries = outer.inputSeries
        
        def generateTwoDSeries(self, log_x:float) -> TwoDSeries:
            mask = rdp(self.inputSeries.getMatrix(), epsilon = 10**log_x, algo="iter", return_mask=True)
            maskedData = self.inputSeries.getMatrix()[mask]
            splitData = np.hsplit(maskedData, 2)
            xAxis = np.transpose(splitData[0])[0]
            yAxis = np.transpose(splitData[1])[0]

            return(TwoDSeries(x_inputSeries=xAxis, y_inputSeries=yAxis))

        def estimateBIC(self, log_x:float) -> float:

            twoDSeries = self.generateTwoDSeries(log_x)

            k = len(twoDSeries.x_inputSeries)
            t = len(self.inputSeries.x_inputSeries)

            if(k > 3 and t > k):
                fStar = interpolate.InterpolatedUnivariateSpline(twoDSeries.x_inputSeries, twoDSeries.y_inputSeries)

                sse = 0
                sumysq = 0
                sumy = 0
                for idx in range(t):
                    x = self.inputSeries.x_inputSeries[idx]
                    y = self.inputSeries.y_inputSeries[idx]
                    yStar = fStar(x)
                    residual = (y - yStar)

                    if(residual < 1e-8):
                        residual = 0

                    sse += residual*residual
                    sumysq += y*y
                    sumy += y


                syy = sumysq - (1/t)*sumy*sumy

                rSqr = 1 - ((t-1)/(t-k))*(sse/syy)

                bic = (t*np.log(sse/t) + (k)*np.log(t)) - log_x
            else:
                bic = 0.0

            return(bic)

        def estimate(self, log_x:float) -> float:

            bic = self.estimateBIC(log_x=log_x)
            
            return(bic)