import numpy as np
import scipy.integrate as integrate
from scipy.interpolate import UnivariateSpline

from src.stratification.abstractquantizer import AbstractQuantizer
from src.stratification.quantization_class import Quantization
from src.stratification.quantizationparameter_class import QuantizationParameter


class EqualAreaQuantizer(AbstractQuantizer):
    
    def generateQuantization(self, quantizationParameter: QuantizationParameter) -> Quantization:
        
        return self.wrapper_logadjust(
            func=self.operation, quantizationParameter=quantizationParameter
        )


    def operation(self, tmpX, tmpY, quantizationParameter: QuantizationParameter):
        # ===========================================================
        # Quantization
        if quantizationParameter.nQuant is None:
            raise Exception("quantizationParameter.nQuant, can't be none")

        nQuant = quantizationParameter.nQuant

        linearSpace = np.linspace(0.0, 1.0, nQuant)

        # generate CDF/ICDF
        ecdf = np.cumsum(tmpY)
        ecdf = ecdf / ecdf[-1]

        # interpolator
        icdf = UnivariateSpline(ecdf, tmpX)
        xQuantEdge = icdf(linearSpace)

        # =======================================================
        # process
        denArray = np.zeros(len(xQuantEdge) - 1)
        yNew = np.zeros(len(xQuantEdge) - 1)

        for jdx in range(len(xQuantEdge) - 1):
            start = xQuantEdge[jdx]
            stop = xQuantEdge[jdx + 1]

            den = integrate.quad(lambda x: self.funcf(x), start, stop)
            num = integrate.quad(lambda x: self.funcfx(x), start, stop)

            if den[0] is np.NAN:
                raise Exception("Denom is Nan, breaking loop")

            denArray[jdx] = den[0]
            yNew[jdx] = num[0] / den[0]

        # ===========================================================
        # reset

        return (xQuantEdge, yNew)
