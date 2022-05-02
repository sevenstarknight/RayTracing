import numpy as np

from src.stratification.twodseries_class import TwoDSeries

class GriddedRealDistribution():
    def __init__(self, inputSeries: TwoDSeries):
        self.inputSeries = inputSeries

        self.pdfValues = inputSeries.y_inputSeries
        self.cdfValues = self.cumTrapzFast(inputSeries.y_inputSeries, 
        (inputSeries.x_inputSeries[1] - inputSeries.x_inputSeries[0])/2)

        factor = 1.0/self.cdfValues[-1]

        self.pdfValues = self.pdfValues/factor
        self.cdfValues = self.cdfValues/factor

    def cumTrapzFast(self, f : np.array, delta : float) -> np.array:

        arg1 = np.cumsum(f)
        
        argList = []
        argList.append(0)

        for indx in range(1, len(arg1)):
            argList.append(arg1[indx-1] - f[0])
        arg2 = np.array(argList)

        fBig = arg1 + arg2
        return(fBig*delta)
