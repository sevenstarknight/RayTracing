import numpy as np
import scipy.integrate as integrate
from scipy import interpolate
import logging

from src.stratification.abstractquantizer import AbstractQuantizer
from src.stratification.quantization_class import Quantization
from src.stratification.twodseries_class import TwoDSeries

MAXITER = 100000
LOGGER = logging.getLogger("mylogger")

class LloydMaxQuantizer(AbstractQuantizer):

    def generateQuantization(self, nQuant : int) -> Quantization:
        xMin = np.amin(self.inputSeries.x_inputSeries)
        xMax = np.amax(self.inputSeries.x_inputSeries)

        yInitialization = np.linspace(xMin, xMax, nQuant)


    def generateQuantization(self, yInitialization: np.array):
        qprior = yInitialization

        lowerBound = np.amin(self.inputSeries.x_inputSeries)
        upperBound = np.amax(self.inputSeries.x_inputSeries)

        boundaryOld = self.generateBOld(qnow = qprior, lowerBound= lowerBound, upperBound = upperBound)

        distoritionPrior = 0
        denArray = []
        for idx in range(MAXITER):
            qnow = []
            denArray = []

            distoritionNow = 0

            for jdx in range(len(boundaryOld) - 1):
                start = boundaryOld[jdx]
                stop = boundaryOld[jdx + 1]

                den = integrate.quad(lambda x: self.funcf(x), start, stop)
                num = integrate.quad(lambda x: self.funcfx(x), start, stop)

                if(den[0] is np.NAN):
                    raise Exception("Denom is Nan, breaking loop")

                denArray.append(den)
                qnow.append(num/den)

                mseEstimate = self.MseEstimate(self, qnow[jdx])
                distoritionNow += integrate.quad(lambda x: mseEstimate.estimate(x), start, stop)

            qprior = qnow
            boundaryOld = self.generateBOld(qnow, lowerBound, upperBound)

            delta = np.abs(distoritionNow - distoritionPrior)/distoritionPrior

            if(delta < 1e-6):
                LOGGER.info("Final Iteration #: " + idx)
                LOGGER.info("Lloyd Max Converged: " + delta)
                break

            distoritionPrior = distoritionNow

            if(idx % 500 == 0):
                LOGGER.debug("Current Iteration #: " + idx)

            if(idx == MAXITER - 2):
                LOGGER.debug("Lloyd Max didn't converge" )





    def generateBOld(qnow: np.array, lowerBound: float, upperBound:float)->np.array:
        qi = qnow[1:-1]
        qiminus1 = qnow[0,-2]

        tmp = (qi + qiminus1)/2.0

        bold =[]
        bold.append(lowerBound)
        bold.append(tmp)
        bold.append(upperBound)

        return(np.array(bold))

    class MseEstimate(object):
        def __init__(self, outer:'LloydMaxQuantizer', y_i: float,):
            self.y_i = y_i
            self.outer = outer
        
        def estimate(self, x:float) -> float:
            return((self.y_i-x)*(self.y_i-x)*self.outer.funcf(x))