from scipy import constants
import numpy as np
# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj

# ====================================================
# local imports
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.indexrefractionmodels.indexofrefractiongenerator import IndexOfRefractionGenerator
from src.bindings.timeandlocation_class import TimeAndLocation
from src.bindings.ionospherestate_class import IonosphereState
from src.bindings.satelliteinformation_class import SatelliteInformation
from src.positional.satellitepositiongenerator import SatellitePositionGenerator
from src.stratification.twodseries_class import TwoDSeries
from src.stratification.stratificationmethod_enum import StratificationMethod
from src.stratification.equalareaquantizer import EqualAreaQuantizer
from src.stratification.lloydmaxquantizer import LloydMaxQuantizer
from src.stratification.rdpquantizer import RDPQuantizer
from src.stratification.equalareaquantizer import EqualAreaQuantizer
from src.stratification.quantizationparameter_class import QuantizationParameter
from src.stratification.decimationquantizer import DecimationQuantizer

# ====================================================
# constants
ECEF = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
LLA = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')

class StratificationOptimizer():

    def __init__(self, timeAndLocation: TimeAndLocation, dispersionModel: DispersionModel, transportMode: TransportMode):
        self.timeAndLocation = timeAndLocation
        self.dispersionModel = dispersionModel
        self.transportMode = transportMode

    def generateHeightModel(self, freq_Hz: float, quantizationParameter : QuantizationParameter,
    satelliteInformation: SatelliteInformation, ionosphereState : IonosphereState) -> list[float]:
        satPosGenerator = SatellitePositionGenerator(satelliteInformation)

        # Initial Starting Point
        sat_ECEF = satPosGenerator.estimatePosition_ECEF(
            self.timeAndLocation.eventTime_UTC)

        sat_lat, sat_lon, sat_alt = pyproj.transform(
            ECEF, LLA, sat_ECEF.x_m, sat_ECEF.y_m, sat_ECEF.z_m, radians=False)

        initialHeights_m = np.linspace(self.timeAndLocation.eventLocation_LLA.altitude_m, sat_alt, 100)

        indexOfRefractionGenerator = IndexOfRefractionGenerator(
            frequency_hz=freq_Hz, dispersionModel=self.dispersionModel, transportMode=self.transportMode)

        indexN = indexOfRefractionGenerator.estimateIndexN(startTimeAndLocation=self.timeAndLocation,
        heightStratification_m=initialHeights_m, sat_ECEF=sat_ECEF, ionosphereState=ionosphereState)

        indexNReal = np.zeros(len(indexN))
        for idx in range(len(indexN)):
            indexNReal[idx] = indexN[idx].real

        testSeries = TwoDSeries(initialHeights_m, indexNReal)

        if(quantizationParameter.stratificationMethod is StratificationMethod.EQUALAREA_MODEL):
            quantizer = EqualAreaQuantizer(testSeries)
        elif(quantizationParameter.stratificationMethod is StratificationMethod.LLOYDMAX_MODEL):
            quantizer = LloydMaxQuantizer(testSeries)
        elif(quantizationParameter.stratificationMethod is StratificationMethod.RDP_MODEL):
            quantizer = RDPQuantizer(testSeries)
        elif(quantizationParameter.stratificationMethod is StratificationMethod.DECIMATION_MODEL):
            quantizer = DecimationQuantizer(testSeries)
        else:
            raise Exception("Stratification method provided unknown")

        quantization = quantizer.generateQuantization(quantizationParameter)
        heights_m = quantization.representationPoints.tolist()
        return(heights_m)