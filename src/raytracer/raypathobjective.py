import math
import logging

# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj

# ====================================================
# local imports
from src.raytracer.raytracer import RayTracer
from src.bindings.coordinates_class import ECEF_Coord
from src.bindings.timeandlocation_class import TimeAndLocation
from src.positional.satellitepositiongenerator import SatellitePositionGenerator
from src.indexrefractionmodels.indexofrefractiongenerator import IndexOfRefractionGenerator

# ====================================================
# constants
ECEF = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
LLA = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
LOGGER = logging.getLogger("mylogger")


class RayPathObjective():
    def __init__(self, freq_hz: float, heights_m: list[float], timeAndLocation: TimeAndLocation,
                 satPosGen: SatellitePositionGenerator, indexOfRefractionGenerator: IndexOfRefractionGenerator):
        self.heights_m = heights_m
        self.satPosGen = satPosGen
        self.timeAndLocation = timeAndLocation
        self.rayTracer = RayTracer(timeAndLocation)
        # ============================================================================
        # Initial Starting Point
        self.sat_ECEF = self.satPosGen.estimatePosition_ECEF(
            timeAndLocation.eventTime_UTC)

        self.indexN = indexOfRefractionGenerator.estimateIndexN(
            startTimeAndLocation=timeAndLocation, heightStratification_m=heights_m, sat_ECEF=self.sat_ECEF)

    def objectiveFunction(self, params: list[float]) -> float:
        # initial parameters
        stateList = self.rayTracer.execute(self.heights_m, self.indexN, params)

        # find last point in the ray
        hypoSat_LLA = stateList[-1].lla

        x_m, y_m, z_m = pyproj.transform(
            LLA, ECEF, hypoSat_LLA.lon_deg, hypoSat_LLA.lat_deg, hypoSat_LLA.altitude_m, radians=False)
        hypoSat_ECEF = ECEF_Coord(x_m, y_m, z_m)

        delta = ECEF_Coord.subtract(self.sat_ECEF, hypoSat_ECEF).magnitude()
        # =================================
        # Log Barrier (I think there is a better way to do this)
        az, el = params
        topEleBound = 0.01*math.log(90.1 - el)
        bottomEleBound = 0.01*math.log(abs(-90.1 - el))

        loss = delta - topEleBound - bottomEleBound
        return(loss)
