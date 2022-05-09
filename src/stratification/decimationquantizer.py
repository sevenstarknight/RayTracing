
from src.stratification.abstractquantizer import AbstractQuantizer
from src.stratification.quantization_class import Quantization
from src.stratification.quantizationparameter_class import QuantizationParameter


class DecimationQuantizer(AbstractQuantizer):

    def generateQuantization(self, quantizationParameter : QuantizationParameter) -> Quantization:
        if(quantizationParameter.nQuant is None):
            raise Exception("quantizationParameter.nQuant, can't be none")
            
        nQuant = quantizationParameter.nQuant
        
        if(nQuant != 0):
            xQuantEdge = self.inputSeries.x_inputSeries[::nQuant]
            yNew = self.inputSeries.y_inputSeries[::nQuant]
        else:
            xQuantEdge = self.inputSeries.x_inputSeries
            yNew = self.inputSeries.y_inputSeries

        return(Quantization(xQuantEdge, yNew))