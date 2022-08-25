import scipy.optimize as optimize


# ====================================================
# local imports
from src.bindings.timeandlocation_class import TimeAndLocation
from src.bindings.ionospherestate_class import IonosphereState
from src.bindings.satelliteinformation_class import SatelliteInformation
from src.positional.locationconverter import convertToAER

from src.raytracer.raytracer import RayTracer
from src.raytracer.raypathobjective import RayPathObjective

from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.indexrefractionmodels.indexofrefractiongenerator import IndexOfRefractionGenerator
from src.positional.satellitepositiongenerator import SatellitePositionGenerator
from src.rayvector_class import RayVector


class RayPathOptimizer():

    def __init__(self, freq_hz: float, timeAndLocation: TimeAndLocation,
                 heights_m: list[float], dispersionModel: DispersionModel, 
                 transportMode: TransportMode, ionosphereState: IonosphereState):
        self.freq_hz = freq_hz
        self.timeAndLocation = timeAndLocation
        self.heights_m = heights_m
        self.ionosphereState = ionosphereState

        self.indexOfRefractionGenerator = IndexOfRefractionGenerator(
            frequency_hz=freq_hz, dispersionModel=dispersionModel, transportMode=transportMode,
            startTimeAndLocation=timeAndLocation, ionosphereState=ionosphereState)

    def optimize(self, satelliteInformation: SatelliteInformation) -> list[RayVector]:

        satPosGenerator = SatellitePositionGenerator(satelliteInformation)

        # Initial Starting Point
        sat_ECEF = satPosGenerator.estimatePosition_ECEF(
            self.timeAndLocation.eventTime_UTC)

        aer = convertToAER(ecef=sat_ECEF,lla=self.timeAndLocation.eventLocation_LLA)
       
        # optimization
        initialGuess = [aer.az_deg, aer.ele_deg]

        objectiveF = RayPathObjective(heights_m=self.heights_m, satPosGen=satPosGenerator,
                                      indexOfRefractionGenerator=self.indexOfRefractionGenerator, timeAndLocation=self.timeAndLocation)

        result = optimize.minimize(objectiveF.objectiveFunction, initialGuess)

        # =============================================================================
        # construct the atmospheric model
        indexN = self.indexOfRefractionGenerator.estimateIndexN(
            heightStratification_m=self.heights_m, sat_ECEF=sat_ECEF)

        # based on the results, generate optimal ray
        rayTracer = RayTracer(
            timeAndLocation=self.timeAndLocation, heights_m=self.heights_m, indexN=indexN)

        rayVectors = rayTracer.execute(params=[result.x[1], result.x[0]])

        return(rayVectors)
