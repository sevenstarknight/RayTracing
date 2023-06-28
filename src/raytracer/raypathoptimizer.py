import scipy.optimize as optimize
from scipy.optimize import minimize, LinearConstraint

# ====================================================
# local imports
from src.bindings.positional.timeandlocation_class import TimeAndLocation
from src.bindings.models.ionospherestate_class import IonosphereState
from src.bindings.positional.satelliteinformation_class import SatelliteInformation
from src.bindings.raytracer.rayvector_class import RayVector
from src.positional.locationconverter_computations import convertToAER
from src.bindings.positional.coordinates_class import AER_Coord, ECEF_Coord

from src.raytracer.raytracer import RayTracer
from src.raytracer.raypathobjective import RayPathObjective

from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.indexrefractionmodels.indexofrefractiongenerator import (
    IndexOfRefractionGenerator,
)
from src.positional.satellitepositiongenerator import SatellitePositionGenerator


class RayPathOptimizer:
    def __init__(
        self,
        freq_hz: float,
        timeAndLocation: TimeAndLocation,
        heights_m: list[float],
        dispersionModel: DispersionModel,
        transportMode: TransportMode,
        ionosphereState: IonosphereState,
    ):
        self.freq_hz = freq_hz
        self.timeAndLocation = timeAndLocation
        self.heights_m = heights_m
        self.ionosphereState = ionosphereState

        self.indexOfRefractionGenerator = IndexOfRefractionGenerator(
            frequency_hz=freq_hz,
            dispersionModel=dispersionModel,
            transportMode=transportMode,
            startTimeAndLocation=timeAndLocation,
            ionosphereState=ionosphereState,
        )

    def optimize(self, satelliteInformation: SatelliteInformation) -> list[RayVector]:
        satPosGenerator = SatellitePositionGenerator(satelliteInformation)

        # Initial Starting Point
        sat_ECEF: ECEF_Coord = satPosGenerator.estimatePosition_ECEF(
            self.timeAndLocation.eventTime_UTC
        )

        aer: AER_Coord = convertToAER(
            ecef=sat_ECEF, lla=self.timeAndLocation.eventLocation_LLA
        )

        # optimization
        objectiveF = RayPathObjective(
            heights_m=self.heights_m,
            satPosGen=satPosGenerator,
            indexOfRefractionGenerator=self.indexOfRefractionGenerator,
            timeAndLocation=self.timeAndLocation,
        )

        initialGuess = [aer.az_deg, aer.ele_deg]
        # no azimuthal bounds, but bound elevation -90 to 90
        bnds = ((None, None), (-90, 90))
        # tol to a meter
        result = minimize(
            objectiveF.objectiveFunction,
            x0=initialGuess,
            method='Nelder-Mead',
            bounds = bnds,
            tol = 1e-3
        )

        # =============================================================================
        # construct the atmospheric model
        indexNs: list[complex] = self.indexOfRefractionGenerator.estimateIndexN(
            heightStratification_m=self.heights_m, sat_ECEF=sat_ECEF
        )

        # based on the results, generate optimal ray
        rayTracer = RayTracer(
            timeAndLocation=self.timeAndLocation,
            heights_m=self.heights_m,
            indexNs=indexNs,
        )

        rayVectors = rayTracer.execute(params=[result.x[1], result.x[0]])

        return rayVectors
