import numpy as np

# ====================================================
# local imports
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.indexrefractionmodels.indexofrefractiongenerator import IndexOfRefractionGenerator
from src.bindings.positional.timeandlocation_class import TimeAndLocation
from src.bindings.models.ionospherestate_class import IonosphereState
from src.bindings.positional.satelliteinformation_class import SatelliteInformation
from src.positional.locationconverter_computations import LocationConverterComputation
from src.positional.satellitepositiongenerator import SatellitePositionGenerator
from src.stratification.quantization_class import Quantization
from src.stratification.twodseries_class import TwoDSeries
from src.stratification.stratificationmethod_enum import StratificationMethod
from src.stratification.equalareaquantizer import EqualAreaQuantizer
from src.stratification.lloydmaxquantizer import LloydMaxQuantizer
from src.stratification.rdpquantizer import RDPQuantizer
from src.stratification.equalareaquantizer import EqualAreaQuantizer
from src.stratification.quantizationparameter_class import QuantizationParameter
from src.stratification.decimationquantizer import DecimationQuantizer


class StratificationOptimizer():

    _exoAtmoHeights_m = np.array([0.467e4, 0.783e4, 1.100e4, 1.416e4, 1.733e4,
                                  2.020e4, 2.050e4, 2.366e4, 2.680e4, 3.000e4])

    def __init__(self, timeAndLocation: TimeAndLocation, dispersionModel: DispersionModel, transportMode: TransportMode):
        self.timeAndLocation = timeAndLocation
        self.dispersionModel = dispersionModel
        self.transportMode = transportMode

    def generateHeightModel(self, freq_Hz: float, quantizationParameter: QuantizationParameter,
                            satelliteInformation: SatelliteInformation, ionosphereState: IonosphereState) -> list[float]:
        satPosGenerator = SatellitePositionGenerator(satelliteInformation)

        # Initial Starting Point
        sat_ECEF = satPosGenerator.estimatePosition_ECEF(
            self.timeAndLocation.eventTime_UTC)

        sat_LLA = LocationConverterComputation.convertFromECEFtoLLA(ecef=sat_ECEF)

        initialHeights_m = np.linspace(60e3, 1100e3, 1000)

        initialHeights_m = np.append(
            initialHeights_m, self.timeAndLocation.eventLocation_LLA.altitude_m)
        initialHeights_m = np.append(initialHeights_m, self._exoAtmoHeights_m)
        initialHeights_m = np.append(initialHeights_m, sat_LLA.altitude_m)
        initialHeights_m.sort()

        # this height should be the last stop
        filtered = filter(lambda x: x <= sat_LLA.altitude_m, initialHeights_m)
        initialHeights_m = np.array(list(filtered))

        indexOfRefractionGenerator = IndexOfRefractionGenerator(
            frequency_hz=freq_Hz, dispersionModel=self.dispersionModel, transportMode=self.transportMode,
            ionosphereState=ionosphereState, startTimeAndLocation=self.timeAndLocation)

        indexNs = indexOfRefractionGenerator.estimateIndexN(
            heightStratification_m=initialHeights_m, sat_ECEF=sat_ECEF)

        indexNReal_list = [x.real for x in indexNs]
        indexNReal = np.array(indexNReal_list)

        testSeries = TwoDSeries(
            x_inputSeries=initialHeights_m, y_inputSeries=indexNReal)

        if (quantizationParameter.stratificationMethod is StratificationMethod.EQUALAREA_MODEL):
            quantizer = EqualAreaQuantizer(inputSeries=testSeries)
        elif (quantizationParameter.stratificationMethod is StratificationMethod.LLOYDMAX_MODEL):
            quantizer = LloydMaxQuantizer(inputSeries=testSeries)
        elif (quantizationParameter.stratificationMethod is StratificationMethod.RDP_MODEL):
            quantizer = RDPQuantizer(inputSeries=testSeries)
        elif (quantizationParameter.stratificationMethod is StratificationMethod.DECIMATION_MODEL):
            quantizer = DecimationQuantizer(inputSeries=testSeries)
        else:
            raise Exception("Stratification method provided unknown")

        quantization : Quantization = quantizer.generateQuantization(
            quantizationParameter=quantizationParameter)
        heights_m = quantization.representationPoints.tolist()

        heights_np_m = np.array(heights_m)
        heights_np_m = np.append(heights_np_m, sat_LLA.altitude_m)
        heights_np_m.sort()
        
        filtered = filter(lambda x: x <= sat_LLA.altitude_m, heights_np_m)
        return list(filtered)

