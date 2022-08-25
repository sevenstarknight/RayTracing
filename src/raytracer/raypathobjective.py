import math

# ====================================================
# local imports
from src.raytracer.raytracer import RayTracer
from src.bindings.coordinates_class import ECEF_Coord
from src.bindings.timeandlocation_class import TimeAndLocation
from src.positional.satellitepositiongenerator import SatellitePositionGenerator
from src.indexrefractionmodels.indexofrefractiongenerator import IndexOfRefractionGenerator

from src.logger.simlogger import get_logger
from src.rayvector_class import RayVector
LOGGER = get_logger(__name__)


class RayPathObjective():
    def __init__(self, heights_m: list[float], timeAndLocation: TimeAndLocation,
                 satPosGen: SatellitePositionGenerator,
                 indexOfRefractionGenerator: IndexOfRefractionGenerator):

        self.heights_m: list[float] = heights_m
        self.satPosGen: SatellitePositionGenerator = satPosGen
        self.timeAndLocation: TimeAndLocation = timeAndLocation
        # ============================================================================
        # Initial Starting Point
        self.sat_ECEF: ECEF_Coord = satPosGen.estimatePosition_ECEF(
            currentDateTime=timeAndLocation.eventTime_UTC)

        indexN: list[complex] = indexOfRefractionGenerator.estimateIndexN(
            heightStratification_m=heights_m, sat_ECEF=self.sat_ECEF)

        # ============================================================================
        self.rayTracer: RayTracer = RayTracer(
            timeAndLocation=timeAndLocation, heights_m=heights_m, indexN=indexN)

    def objectiveFunction(self, params: list[float]) -> float:
        # initial parameters
        stateList: list[RayVector] = self.rayTracer.execute(params=params)

        # find last point in the ray
        hypoSat_ECEF: ECEF_Coord = stateList[-1]._ecef_p2

        delta: float = ECEF_Coord.subtract(
            ecef1=self.sat_ECEF, ecef2=hypoSat_ECEF).magnitude()
        # =================================
        # Log Barrier (I think there is a better way to do this)
        az, el = params
        topEleBound = 0.01*math.log(90.1 - el)
        bottomEleBound = 0.01*math.log(abs(-90.1 - el))

        loss = delta - topEleBound - bottomEleBound

        return(loss)
