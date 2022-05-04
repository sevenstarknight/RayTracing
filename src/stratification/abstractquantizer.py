from abc import ABC, abstractmethod

from scipy import interpolate
import scipy.integrate as integrate

from src.stratification.twodseries_class import TwoDSeries
from src.stratification.quantizationparameter_class import QuantizationParameter

class AbstractQuantizer(ABC):

    def __init__(self, inputSeries: TwoDSeries):
        self.inputSeries = inputSeries
        self.generateSplines()

        super().__init__()

    def generateSplines(self):
        self.funcInput = interpolate.InterpolatedUnivariateSpline(self.inputSeries.x_inputSeries, self.inputSeries.y_inputSeries)

        # estimate f(x)
        start = self.inputSeries.x_inputSeries[0]
        end = self.inputSeries.x_inputSeries[-1]

        areaY = integrate.quad(lambda x : self.funcInput(x), start, end)
        fSeries = TwoDSeries(self.inputSeries.x_inputSeries, self.inputSeries.y_inputSeries/areaY[0])
        xfSeries = TwoDSeries(self.inputSeries.x_inputSeries, self.inputSeries.x_inputSeries*fSeries.y_inputSeries)

        # estimate f(x) and x*f(x)
        self.funcf = interpolate.InterpolatedUnivariateSpline(self.inputSeries.x_inputSeries, fSeries.y_inputSeries)

        self.funcfx = interpolate.InterpolatedUnivariateSpline(xfSeries.x_inputSeries, xfSeries.y_inputSeries)

    @abstractmethod
    def generateQuantization(self, quantizationParameter : QuantizationParameter):
        pass