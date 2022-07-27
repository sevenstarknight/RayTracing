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

# ====================================================
# constants
ECEF = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
LLA = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')

class EstimateRayPathEffects():

    def __init__(self, timeAndLocation: TimeAndLocation, dispersionModel: DispersionModel, transportMode: TransportMode):
        self.timeAndLocation = timeAndLocation
        self.dispersionModel = dispersionModel
        self.transportMode = transportMode


    def estimate(self, freq_Hz: float, quantizationParameter: QuantizationParameter, 
    satelliteInformation: SatelliteInformation, ionosphereState : IonosphereState) -> TransIonosphereEffects:

        # ======================================================
        stratificationOptimizer = StratificationOptimizer(dispersionModel=self.dispersionModel, 
        timeAndLocation=self.timeAndLocation, transportMode=self.transportMode)

        heights_m = stratificationOptimizer.generateHeightModel(freq_Hz=freq_Hz, quantizationParameter=quantizationParameter,
        ionosphereState=ionosphereState,satelliteInformation=satelliteInformation)

        # ======================================================
        # Generate Ray State
        optimizer = RayPathOptimizer(
            freq_hz=freq_Hz, timeAndLocation=self.timeAndLocation, heights_m=heights_m, dispersionModel=self.dispersionModel, 
            transportMode=self.transportMode, ionosphereState=ionosphereState)

        rayStates = optimizer.optimize(satelliteInformation)

        totalIonoLoss_db = 0
        totalIonoDelay_sec = 0
        totalGeoDistance_m = 0

        for idx in range(len(rayStates) - 1):
            s12 =  rayStates[idx+1].lla.altitude_m - rayStates[idx].lla.altitude_m

            totalGeoDistance_m = totalGeoDistance_m + s12

            totalIonoDelay_sec = totalIonoDelay_sec + \
                (1 - rayStates[idx].nIndex.real)*s12

            totalIonoLoss_db = totalIonoLoss_db + 8.68 * \
                (2*constants.pi*freq_Hz/constants.c) * \
                rayStates[idx].nIndex.imag*s12

        rayEffects = TransIonosphereEffects(
            rayStates, totalIonoDelay_sec, totalIonoLoss_db, totalGeoDistance_m)
            
        return(rayEffects)
