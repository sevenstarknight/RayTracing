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
from src.bindings.satelliteinformation_class import SatelliteInformation
from src.raytracer.raypathoptimizer import RayPathOptimizer

# ====================================================
# constants
ECEF = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
LLA = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


class EstimateRayPathEffects():

    def __init__(self, timeAndLocation: TimeAndLocation, dispersionModel: DispersionModel, transportMode: TransportMode):
        self.timeAndLocation = timeAndLocation
        self.dispersionModel = dispersionModel
        self.transportMode = transportMode

    def estimate(self, freq_Hz: float, satelliteInformation: SatelliteInformation) -> TransIonosphereEffects:

        # ======================================================
        heights_m = [0, 100, 1000, 10000, 100000, 1000000]

        # ======================================================
        # Generate Ray State
        optimizer = RayPathOptimizer(
            freq_Hz, self.timeAndLocation, heights_m, self.dispersionModel, self.transportMode)

        rayState = optimizer.optimize(satelliteInformation)

        totalIonoLoss_db = 0
        totalIonoDelay_sec = 0
        for idx in range(len(rayState) - 1):
            s12 = rayState[idx-1].lla.altitude_m - rayState[idx].lla.altitude_m

            totalIonoDelay_sec = totalIonoDelay_sec + \
                (1 - rayState[idx].nIndex.real)*s12

            totalIonoLoss_db = totalIonoLoss_db + 8.68 * \
                (2*constants.pi*freq_Hz/constants.c) * \
                rayState[idx].nIndex.imag*s12

        rayEffects = TransIonosphereEffects(
            rayState, totalIonoDelay_sec, totalIonoLoss_db)
            
        return(rayEffects)
