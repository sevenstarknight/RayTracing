import math
import cmath

# ====================================================
# local imports
from src.raytracer.raytracer_computations import computeGeocentricRadius, computeNewIntersection, computeEntryAngle, generatePositionAndVector

from src.bindings.raytracer.interface_class import Interface
from src.bindings.raytracer.rayvector_class import RayVector
from src.bindings.raytracer.raystate_class import RayState
from src.bindings.exceptions_class import IntersectException
from src.bindings.positional.coordinates_class import ECEF_Coord
from src.bindings.positional.timeandlocation_class import TimeAndLocation

from src.positional.locationconverter_computations import convertFromECEFtoLLA

from src.logger.simlogger import get_logger
LOGGER = get_logger(__name__)

class RayTracer():
    def __init__(self, timeAndLocation: TimeAndLocation, heights_m: list[float], indexNs: list[complex]):
        self.timeAndLocation = timeAndLocation
        self.heights_m = heights_m
        self.indexNs = indexNs

    def execute(self, params: list[float]) -> list[RayVector]:
        '''
        The ray tracer logic, handles the loop that iterates the ray through layers, 
        inputs are the heights of the layers, the associated index of refraction, and 
        the initial exit state of the ray
        '''
        az, el = params
        if(az < 0 or az > 360):
            LOGGER.warn("Exceeding 0/360 bounds for azimuth")

        # =======================================================
        # Initialize the ray state for the start point
        currentState = RayState(
            exitElevation_deg=el, exitAzimuth_deg=az, lla=self.timeAndLocation.eventLocation_LLA)

        # =================================================================
        rayVectors = []

        for idx in range(100):

            layerOutput: Interface = self.insideLayerOperations(
                currentState, rayVectors)

            if(layerOutput.n_1 == None):
                LOGGER.debug("Done with iterations, jump out of loop")
                break

            currentState: RayState = self.onTheEdgeOperations(
                currentState, layerOutput)

        return(rayVectors)

    def _findNextIntersectPoint(self, currentState: RayState, ecef_p1: ECEF_Coord, sVector_m: ECEF_Coord) -> tuple[ECEF_Coord, float, int]:
        lla_p1 = currentState.lla

        if(currentState.exitElevation_deg > 0):
            # going up
            indx = next(x for x, val in enumerate(
                self.heights_m) if val > currentState.lla.altitude_m)
        else:
            # going down
            indx = len([x for x in self.heights_m if x <
                       currentState.lla.altitude_m]) - 1

        if(len(self.heights_m) <= indx):
            LOGGER.debug("Outside ionosphere")
            return None, None
        else:
            # layer intersection
            newAltitude_m = self.heights_m[indx]

        # ==========================================================================
        # use quadratic equation to determine intersection in ECEF of the next layer based prior intersection and vector
        try:
            ecef_p2 = computeNewIntersection(ecef_p1, sVector_m, newAltitude_m)
        except IntersectException as inst1:
            # no intersection, which means (a) angle is down and (b) it is skipping over the lower layer; intersect with self
            if(lla_p1.altitude_m in self.heights_m):
                newAltitude_m = lla_p1.altitude_m
            else:
                indx = next(x for x, val in enumerate(
                    self.heights_m) if val > lla_p1.altitude_m)
                newAltitude_m = self.heights_m[indx]

            try:
                ecef_p2 = computeNewIntersection(
                    ecef_p1, sVector_m, newAltitude_m)
            except IntersectException as inst2:
                LOGGER.error(inst2.args)
                raise IntersectException("how did we get here?")

        return ecef_p2, newAltitude_m, indx

    def _estimateIndexesAtTransition(self, indx: int, newAltitude_m: float, currentState: RayState) -> tuple[complex, complex]:

        lla_p1 = currentState.lla

        if(lla_p1.altitude_m in self.heights_m):
            # standard heights
            if(newAltitude_m == lla_p1.altitude_m):
                # horizontal transitions
                n_2 = self.indexNs[indx]
                n_1 = self.indexNs[indx - 1]
                LOGGER.debug("horizontal transitions")
            elif(newAltitude_m < lla_p1.altitude_m):
                if(newAltitude_m == min(self.heights_m)):
                    # to ground
                    n_2 = 3.0  # rough estimate
                    n_1 = self.indexNs[indx]
                    LOGGER.debug("bounce off ground")
                else:
                    n_2 = self.indexNs[indx - 1]
                    n_1 = self.indexNs[indx]
                    LOGGER.debug("down transitions")
            elif(newAltitude_m > lla_p1.altitude_m):
                n_2 = self.indexNs[indx]
                n_1 = self.indexNs[indx - 1]
                LOGGER.debug("up transitions")
        else:
            if(newAltitude_m < lla_p1.altitude_m):
                if(indx == 0):
                    # to ground
                    n_2 = 3.0  # rough estimate
                    n_1 = self.indexNs[indx]
                    LOGGER.debug("bounce off ground")
                else:
                    n_2 = self.indexNs[indx - 1]
                    n_1 = self.indexNs[indx]
                    LOGGER.debug("down transitions")
            elif(newAltitude_m > lla_p1.altitude_m):
                n_2 = self.indexNs[indx]
                n_1 = self.indexNs[indx - 1]
                LOGGER.debug("up transitions")

        return (n_1, n_2)

    def insideLayerOperations(self, currentState: RayState, rayVectors: list[RayVector]) -> Interface:
        # ==========================================================================
        # Inside the Layer
        # ==========================================================================
        lla_p1 = currentState.lla

        if(max(self.heights_m) <= lla_p1.altitude_m):
            # exiting the loop
            layerOutput = Interface.from_Empty()
            LOGGER.debug("Exiting the atmosphere")
            return(layerOutput)

        ecef_p1, sVector_m = generatePositionAndVector(currentState)

        # ==========================================================================
        # use quadratic equation to determine intersection in ECEF of the next layer based prior intersection and vector
        ecef_p2, newAltitude_m, indx = self._findNextIntersectPoint(currentState=currentState,
                                                                    ecef_p1=ecef_p1, sVector_m=sVector_m)

        if ecef_p2 == None:
            # exiting the loop
            layerOutput = Interface.from_Empty()
            LOGGER.debug("Exiting the atmosphere")
            return(layerOutput)

        rayVector = RayVector(rayState=currentState, sVector_m=sVector_m, ecef_p1=ecef_p1,
                              ecef_p2=ecef_p2, newAltitude_m=newAltitude_m, n_1=n_1)

        rayVectors.append(rayVector)
        # ===================================================================
        # determine index transition
        n_1, n_2 = self._estimateIndexesAtTransition(indx=indx, currentState=currentState)

        # ===================================================================
        lla_p2 = convertFromECEFtoLLA(ecef=ecef_p2)
        lla_p2.setAltitude(newAlitude_m=newAltitude_m)

        # estimate entry angle onto the curved layers
        entryAngle_deg = computeEntryAngle(exitElevation=currentState.exitElevation_deg,
                                           ecef_p1=ecef_p1, ecef_p2=ecef_p2, lla_p1=lla_p1, lla_p2=lla_p2)

        layerOutput = Interface(
            n_1=n_1, n_2=n_2, entryAngle_deg=entryAngle_deg, newAltitude_m=newAltitude_m,
            intersection_LLA=lla_p2)

        return(layerOutput)

    def onTheEdgeOperations(self, currentState: RayState, layerOutput: Interface) -> RayState:
        n_1 = layerOutput.n_1
        n_2 = layerOutput.n_2

        entryAngle_deg = layerOutput.entryAngle_deg
        newAltitude_m = layerOutput.newAltitude_m
        lla_p2 = layerOutput.intersection_LLA

        # TODO, determine if refraction is occuring
        if(newAltitude_m == 0.0):
            # bounce off ground
            exitAngle_deg = -entryAngle_deg
            # convert to elevation pointing up
            currentState = RayState(
                90.0 - exitAngle_deg, currentState.exitAzimuth_deg, lla_p2, n_1)
            LOGGER.debug("bounce off ground: flip direction of ray")
        else:
            f_2 = computeGeocentricRadius(lla_p2) + lla_p2.altitude_m
            f_1 = computeGeocentricRadius(
                currentState.lla) + currentState.lla.altitude_m

            # Snell's with ellipsoidal layers
            argument = n_1*f_1*math.sin(math.radians(entryAngle_deg))/(n_2*f_2)

            if(argument.real > 1.0):
                # past critical angle -> reflection
                exitAngle_deg = -entryAngle_deg
                LOGGER.debug("past critical angle -> reflection")
                # convert to elevation pointing down
                currentState = RayState(-90.0 - exitAngle_deg,
                                        currentState.exitAzimuth_deg, lla_p2, n_1)
            else:
                # refraction
                refracAngle_rad = cmath.asin(argument)
                exitAngle_deg = math.degrees(refracAngle_rad.real)

                if(refracAngle_rad.imag > 0):
                    LOGGER.info("complex angle present")

                # store into a ray state
                if(exitAngle_deg >= 0):
                    # convert to elevation pointing up
                    currentState = RayState(
                        90.0 - exitAngle_deg, currentState.exitAzimuth_deg, lla_p2, n_2)
                else:
                    # convert to elevation pointing down
                    currentState = RayState(-90.0 - exitAngle_deg,
                                            currentState.exitAzimuth_deg, lla_p2, n_2)

        return(currentState)
