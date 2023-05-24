from abc import ABC, abstractmethod

from scipy.interpolate import InterpolatedUnivariateSpline
import scipy.integrate as integrate
from src.stratification.quantization_class import Quantization

from src.stratification.twodseries_class import TwoDSeries
from src.stratification.quantizationparameter_class import QuantizationParameter

class AbstractQuantizer(ABC):

    def __init__(self, inputSeries: TwoDSeries) -> None:
        self.inputSeries = inputSeries
        self.generateSplines()

    def generateSplines(self) -> None:
        self.funcInput = InterpolatedUnivariateSpline(self.inputSeries.x_inputSeries, self.inputSeries.y_inputSeries)

        # estimate f(x)
        start = self.inputSeries.x_inputSeries[0]
        end = self.inputSeries.x_inputSeries[-1]

        areaY = integrate.quad(lambda x : self.funcInput(x), start, end)
        fSeries = TwoDSeries(x_inputSeries=self.inputSeries.x_inputSeries,y_inputSeries= self.inputSeries.y_inputSeries/areaY[0])
        xfSeries = TwoDSeries(x_inputSeries=self.inputSeries.x_inputSeries, y_inputSeries= self.inputSeries.x_inputSeries*fSeries.y_inputSeries)

        # estimate f(x) and x*f(x)
        self.funcf = InterpolatedUnivariateSpline(self.inputSeries.x_inputSeries, fSeries.y_inputSeries)

        self.funcfx = InterpolatedUnivariateSpline(xfSeries.x_inputSeries, xfSeries.y_inputSeries)

    @abstractmethod
    def generateQuantization(self, quantizationParameter : QuantizationParameter) -> Quantization:
        pass