import numpy as np
import scipy.integrate as integrate
from scipy import interpolate
import logging

# ====================================================
# local
from src.stratification.abstractquantizer import AbstractQuantizer
from src.stratification.quantization_class import Quantization

# ====================================================
# constants
MAXITER = 100000
LOGGER = logging.getLogger("mylogger")

class LloydMaxQuantizer(AbstractQuantizer):

    def generateQuantization(self, nQuant : int) -> Quantization:
        lowerBound = np.amin(self.inputSeries.x_inputSeries)
        upperBound = np.amax(self.inputSeries.x_inputSeries)

        qprior = np.linspace(lowerBound, upperBound, nQuant)
        boundaryOld = self.generateBOld(qnow = qprior, lowerBound= lowerBound, upperBound = upperBound)

        distoritionPrior = 1e-6
        denArray = np.zeros(nQuant)
        for idx in range(MAXITER):
            qnow = np.zeros(nQuant)
            denArray = np.zeros(nQuant)

            distoritionNow = 0

            for jdx in range(nQuant):
                start = boundaryOld[jdx]
                stop = boundaryOld[jdx + 1]

                den = integrate.quad(lambda x: self.funcf(x), start, stop)[0]
                num = integrate.quad(lambda x: self.funcfx(x), start, stop)[0]

                if(den is np.NAN):
                    raise Exception("Denom is Nan, breaking loop")

                denArray[jdx] = den
                qnow[jdx] = (num/den)

                mseEstimate = self.MseEstimate(self, qnow[jdx])
                distoritionNow += integrate.quad(lambda x: mseEstimate.estimate(x), start, stop)[0]

            qprior = qnow
            boundaryOld = self.generateBOld(qnow, lowerBound, upperBound)

            delta = np.abs(distoritionNow - distoritionPrior)/distoritionPrior

            if(delta < 1e-3):
                LOGGER.info("Final Iteration #: %s" , str(idx))
                LOGGER.info("Lloyd Max Converged: %s" , str(delta))
                break

            distoritionPrior = distoritionNow

            if(idx % 20 == 0):
                LOGGER.info("Current Iteration #: %s" , str(idx))
                LOGGER.info("Current Delta Distort #: %s" , str(delta))

            if(idx == MAXITER - 2):
                LOGGER.debug("Lloyd Max didn't converge" )

        return(Quantization(boundaryOld, qprior, denArray))

    def generateBOld(self, qnow: np.array, lowerBound: float, upperBound:float)->np.array:
        qi = qnow[1:]
        qiminus1 = qnow[0:-1]

        b_i = (qi + qiminus1)/2.0
        
        bold = np.array(lowerBound)

        bold = np.append(bold, b_i)
        bold = np.append(bold, upperBound)

        return(bold)

    class MseEstimate(object):
        def __init__(self, outer:'LloydMaxQuantizer', y_i: float,):
            self.y_i = y_i
            self.outer = outer
        
        def estimate(self, x:float) -> float:
            return((self.y_i-x)*(self.y_i-x)*self.outer.funcf(x))