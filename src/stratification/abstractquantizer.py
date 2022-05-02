from abc import ABC, abstractmethod

from scipy import interpolate
import scipy.integrate as integrate

from src.stratification.griddedrealdistribution_class import GriddedRealDistribution
from src.stratification.twodseries_class import TwoDSeries


class AbstractQuantizer(ABC):

    def __init__(self, inputSeries: TwoDSeries):
        self.inputSeries = inputSeries
        self.generateInputSeriesSpline()
        self.generateLocalSplines()

        super().__init__()

    def generateInputSeriesSpline(self):
        self.funcInput = interpolate.InterpolatedUnivariateSpline(self.inputSeries.x_inputSeries, self.inputSeries.y_inputSeries)

    def generateLocalSplines(self):
        fPdfDistro = self.getSplineOfPDF()
        pdfY = fPdfDistro.pdfValues

        xfSeries = TwoDSeries(self.inputSeries.x_inputSeries, self.inputSeries.x_inputSeries*pdfY)

        self.funcf = interpolate.InterpolatedUnivariateSpline(self.inputSeries.x_inputSeries, fPdfDistro.pdfValues)

        self.funcfx = interpolate.InterpolatedUnivariateSpline(xfSeries.x_inputSeries, xfSeries.y_inputSeries)


    def getSplineOfPDF(self) -> GriddedRealDistribution:

        start = self.inputSeries.x_inputSeries[0]
        end = self.inputSeries.x_inputSeries[-1]
        startValue = self.funcInput(start)
        endValue = self.funcInput(end)

        areaY = integrate.quad(lambda x : self.funcInput(x), start, end)
        updatedPDF = TwoDSeries(self.inputSeries.x_inputSeries, self.inputSeries.y_inputSeries/areaY[0])
        return(GriddedRealDistribution(updatedPDF))


    @abstractmethod
    def generateQuantization(self, nQuant : int):
        pass