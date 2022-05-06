from scipy import constants

# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj

# ====================================================
# local imports
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.bindings.transionosphereeffects_class import TransIonosphereEffects
from src.bindings.timeandlocation_class import TimeAndLocation
from src.bindings.ionospherestate_class import IonosphereState
from src.bindings.satelliteinformation_class import SatelliteInformation
from src.raytracer.raypathoptimizer import RayPathOptimizer
from src.stratification.stratificationoptimizer import StratificationOptimizer
from src.stratification.quantizationparameter_class import QuantizationParameter
from src.stratification.stratificationmethod_enum import StratificationMethod

# ====================================================
# constants
ECEF = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
LLA = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')

class EstimateRayPathEffects():

    def __init__(self, timeAndLocation: TimeAndLocation, dispersionModel: DispersionModel, transportMode: TransportMode):
        self.timeAndLocation = timeAndLocation
        self.dispersionModel = dispersionModel
        self.transportMode = transportMode


    def estimate(self, freq_Hz: float, satelliteInformation: SatelliteInformation, ionosphereState : IonosphereState) -> TransIonosphereEffects:

        # ======================================================
        stratificationOptimizer = StratificationOptimizer(dispersionModel=self.dispersionModel, 
        timeAndLocation=self.timeAndLocation, transportMode=self.transportMode)

        quantizationParameter = QuantizationParameter(StratificationMethod.DECIMATION_MODEL,nQuant=100)

        heights_m = stratificationOptimizer.generateHeightModel(freq_Hz=freq_Hz, quantizationParameter=quantizationParameter,
        ionosphereState=ionosphereState,satelliteInformation=satelliteInformation)

        #heights_m = [0, 100, 1000, 10000, 100000, 1000000]

        # ======================================================
        # Generate Ray State
        optimizer = RayPathOptimizer(
            freq_Hz, self.timeAndLocation, heights_m, self.dispersionModel, self.transportMode)

        rayStates = optimizer.optimize(satelliteInformation, ionosphereState)

        totalIonoLoss_db = 0
        totalIonoDelay_sec = 0
        for idx in range(len(rayStates) - 1):
            s12 =  rayStates[idx].lla.altitude_m - rayStates[idx-1].lla.altitude_m

            totalIonoDelay_sec = totalIonoDelay_sec + \
                (1 - rayStates[idx].nIndex.real)*s12

            totalIonoLoss_db = totalIonoLoss_db + 8.68 * \
                (2*constants.pi*freq_Hz/constants.c) * \
                rayStates[idx].nIndex.imag*s12

        rayEffects = TransIonosphereEffects(
            rayStates, totalIonoDelay_sec, totalIonoLoss_db)
            
        return(rayEffects)
