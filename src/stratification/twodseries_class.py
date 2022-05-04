import numpy as np
from scipy import interpolate

class TwoDSeries():
    def __init__(self, x_inputSeries: np.array, y_inputSeries: np.array):
        self.x_inputSeries = x_inputSeries
        self.y_inputSeries = y_inputSeries

    def getSpline(self):
        fStar = interpolate.InterpolatedUnivariateSpline(self.x_inputSeries, self.y_inputSeries)
        return(fStar)

    def getMatrix(self)-> np.array:
        return(np.stack((self.x_inputSeries, self.y_inputSeries), axis=-1))

