from scipy import constants


# ====================================================
# local imports
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.bindings.transionosphereeffects_class import TransIonosphereEffects
from src.bindings.positional.timeandlocation_class import TimeAndLocation
from src.bindings.models.ionospherestate_class import IonosphereState
from src.bindings.raytracer.rayvector_class import RayVector
from src.bindings.positional.satelliteinformation_class import SatelliteInformation
from src.raytracer.raypathoptimizer import RayPathOptimizer
from src.stratification.stratificationoptimizer import StratificationOptimizer
from src.stratification.quantizationparameter_class import QuantizationParameter


class EstimateRayPathEffects():

    def __init__(self, timeAndLocation: TimeAndLocation, dispersionModel: DispersionModel, transportMode: TransportMode) -> None:
        self.timeAndLocation = timeAndLocation
        self.dispersionModel = dispersionModel
        self.transportMode = transportMode

    def estimate(self, freq_Hz: float, quantizationParameter: QuantizationParameter,
                 satelliteInformation: SatelliteInformation, ionosphereState: IonosphereState) -> TransIonosphereEffects:

        # ======================================================
        stratificationOptimizer = StratificationOptimizer(dispersionModel=self.dispersionModel,
                                                          timeAndLocation=self.timeAndLocation, transportMode=self.transportMode)

        heights_m = stratificationOptimizer.generateHeightModel(freq_Hz=freq_Hz, quantizationParameter=quantizationParameter,
                                                                ionosphereState=ionosphereState, satelliteInformation=satelliteInformation)

        # ======================================================
        # Generate Ray State
        optimizer = RayPathOptimizer(
            freq_hz=freq_Hz, timeAndLocation=self.timeAndLocation, heights_m=heights_m, dispersionModel=self.dispersionModel,
            transportMode=self.transportMode, ionosphereState=ionosphereState)

        rayVectors: list[RayVector] = optimizer.optimize(satelliteInformation=satelliteInformation)

        totalIonoLoss_db = 0
        totalIonoDelay_sec = 0
        totalGeoDistance_m = 0

        for rayVector in rayVectors:

            s12: float = rayVector.sVector_m.magnitude()

            totalGeoDistance_m = totalGeoDistance_m + s12

            totalIonoDelay_sec = totalIonoDelay_sec + \
                (1 - rayVector.n_1.real)*s12

            totalIonoLoss_db = totalIonoLoss_db + 8.68 * \
                (2*constants.pi*freq_Hz/constants.c) * \
                rayVector.n_1.imag*s12

        rayEffects = TransIonosphereEffects(
            rayVectors=rayVectors, totalIonoDelay_sec=totalIonoDelay_sec,
            totalIonoLoss_db=totalIonoLoss_db, totalGeoDistance_m=totalGeoDistance_m)

        return (rayEffects)
