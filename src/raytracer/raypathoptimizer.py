import scipy.optimize as optimize

# ====================================================
# https://geospace-code.github.io/pymap3d/index.html
import pymap3d

# ====================================================
# local imports
from src.bindings.timeandlocation_class import TimeAndLocation
from src.bindings.satelliteinformation_class import SatelliteInformation

from src.raystate_class import RayState
from src.raytracer.raytracer import RayTracer
from src.raytracer.raypathobjective import RayPathObjective

from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.indexrefractionmodels.indexofrefractiongenerator import IndexOfRefractionGenerator
from src.positional.satellitepositiongenerator import SatellitePositionGenerator


class RayPathOptimizer():

    def __init__(self, freq_hz: float, timeAndLocation: TimeAndLocation, heights_m: list[float], dispersionModel: DispersionModel):
        self.freq_hz = freq_hz
        self.timeAndLocation = timeAndLocation
        self.heights_m = heights_m
        self.indexOfRefractionGenerator = IndexOfRefractionGenerator(
            frequency_hz=freq_hz, dispersionModel=dispersionModel)

    def optimize(self, satelliteInformation: SatelliteInformation) -> list[RayState]:

        satPosGenerator = SatellitePositionGenerator(satelliteInformation)

        # Initial Starting Point
        sat_ECEF = satPosGenerator.estimatePosition_ECEF(
            self.timeAndLocation.eventTime_UTC)

        initialAz_deg, initialEle_deg, initialRange_m = pymap3d.ecef2aer(sat_ECEF.x_m, sat_ECEF.y_m, sat_ECEF.z_m,
                                                                         self.timeAndLocation.eventLocation_LLA.lat_deg, self.timeAndLocation.eventLocation_LLA.lon_deg,
                                                                         self.timeAndLocation.eventLocation_LLA.altitude_m, ell=None, deg=True)

        # optimization
        initialGuess = [initialAz_deg, initialEle_deg]

        objectiveF = RayPathObjective(self.freq_hz,
                                      self.heights_m, self.timeAndLocation, satPosGenerator, self.indexOfRefractionGenerator)
        result = optimize.minimize(objectiveF.objectiveFunction, initialGuess)

        # =============================================================================
        # based on the results, generate optimal ray
        rayTracer = RayTracer(self.timeAndLocation)

        # construct the atmospheric model
        self.indexN = self.indexOfRefractionGenerator.estimateIndexN(startTimeAndLocation=self.timeAndLocation,
                                                                     heightStratification_m=self.heights_m, sat_ECEF=sat_ECEF)

        states = rayTracer.execute(self.heights_m, self.indexN,
                                   [result.x[1], result.x[0]])

        return(states)
