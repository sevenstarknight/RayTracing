import math
from src.positional.locationconverter_computations import convertFromECEFtoLLA

# ====================================================
# local imports
from src.raytracer.raytracer import RayTracer
from src.bindings.positional.coordinates_class import ECEF_Coord
from src.bindings.positional.timeandlocation_class import TimeAndLocation
from src.positional.satellitepositiongenerator import SatellitePositionGenerator
from src.indexrefractionmodels.indexofrefractiongenerator import (
    IndexOfRefractionGenerator,
)
from src.bindings.raytracer.rayvector_class import RayVector


class RayPathObjective:
    def __init__(
        self,
        heights_m: list[float],
        timeAndLocation: TimeAndLocation,
        satPosGen: SatellitePositionGenerator,
        indexOfRefractionGenerator: IndexOfRefractionGenerator,
    ):
        self.heights_m: list[float] = heights_m
        self.satPosGen: SatellitePositionGenerator = satPosGen
        self.timeAndLocation: TimeAndLocation = timeAndLocation
        # ============================================================================
        # Initial Starting Point
        self.sat_ECEF: ECEF_Coord = satPosGen.estimatePosition_ECEF(
            currentDateTime=timeAndLocation.eventTime_UTC
        )

        indexNs: list[complex] = indexOfRefractionGenerator.estimateIndexN(
            heightStratification_m=heights_m, sat_ECEF=self.sat_ECEF
        )

        # ============================================================================
        self.rayTracer: RayTracer = RayTracer(
            timeAndLocation=timeAndLocation, heights_m=heights_m, indexNs=indexNs
        )

    def objectiveFunction(self, params: list[float]) -> float:
        # initial parameters
        stateList: list[RayVector] = self.rayTracer.execute(params=params)

        # find last point in the ray
        hypoSat_ECEF: ECEF_Coord = stateList[-1].ecef_p2

        lla_hypo = convertFromECEFtoLLA(ecef=hypoSat_ECEF)
        lla_sat = convertFromECEFtoLLA(ecef=self.sat_ECEF)

        loss: float = ECEF_Coord.subtract(
            ecef1=self.sat_ECEF, ecef2=hypoSat_ECEF
        ).magnitude()/1000.0

        return loss
