import numpy as np
import scipy.integrate as integrate
from scipy import interpolate

from src.stratification.abstractquantizer import AbstractQuantizer
from src.stratification.quantization_class import Quantization
from src.stratification.twodseries_class import TwoDSeries


class EqualAreaQuantizer(AbstractQuantizer):

    def generateQuantization(self, nQuant : int) -> Quantization:
        linearSpace = np.linspace(0.0, 1.0, nQuant)

        # generate CDF/ICDF
        ecdf = np.cumsum(self.inputSeries.y_inputSeries)
        ecdf = ecdf/ecdf[-1]

        icdf = interpolate.InterpolatedUnivariateSpline(ecdf, self.inputSeries.x_inputSeries)

        xQuantEdge = icdf(linearSpace)
        xQuantEdge[0] = self.inputSeries.x_inputSeries[0]

        denArray = []
        yNew = []

        for jdx in range(len(xQuantEdge) - 1):

            start = xQuantEdge[jdx]
            stop = xQuantEdge[jdx + 1]

            den = integrate.quad(lambda x: self.funcf(x), start, stop)
            num = integrate.quad(lambda x: self.funcfx(x), start, stop)

            if(den[0] is np.NAN):
                raise Exception("Denom is Nan, breaking loop")

            denArray.append(den[0])
            yNew.append(num[0]/den[0])

        return(Quantization(xQuantEdge, np.array(yNew), np.array(denArray)))