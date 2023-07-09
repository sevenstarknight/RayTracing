import math
import cmath
from dataclasses import dataclass
from loguru import logger
from typing import Optional
from src.bindings.raytracer.intersection_class import IntersectionPoint

# ====================================================
# local imports
from src.raytracer.raytracer_computations import RayTracerComputations

from src.bindings.raytracer.interface_class import Interface
from src.bindings.raytracer.rayvector_class import RayVector
from src.bindings.raytracer.raystate_class import RayState
from src.bindings.exceptions_class import IntersectException
from src.bindings.positional.coordinates_class import ECEF_Coord, LLA_Coord
from src.bindings.positional.timeandlocation_class import TimeAndLocation

from src.positional.locationconverter_computations import convertFromECEFtoLLA

MAX_ITER = 1000000

class RayTracer:
    def __init__(
        self,
        timeAndLocation: TimeAndLocation,
        heights_m: list[float],
        indexNs: list[complex],
    ):
        self.timeAndLocation: TimeAndLocation = timeAndLocation
        self.heights_m: list[float] = heights_m
        self.indexNs: list[complex] = indexNs

    def execute(self, params: list[float]) -> list[RayVector]:
        """
        The ray tracer logic, handles the loop that iterates the ray through layers,
        inputs are the heights of the layers, the associated index of refraction, and
        the initial exit state of the ray
        """
        az, el = params
        if az < 0 or az > 360:
            logger.warning("Exceeding 0/360 bounds for azimuth")

        # =======================================================
        # Initialize the ray state for the start point
        currentState = RayState(
            exitElevation_deg=el,
            exitAzimuth_deg=az,
            lla=self.timeAndLocation.eventLocation_LLA,
        )

        # =================================================================
        transitionGenerator = TransitionGenerator(
            currentState=currentState,
            timeAndLocation=self.timeAndLocation,
            heights_m=self.heights_m,
            indexNs=self.indexNs,
        )
        
        rayVectors = []
                      
        for _ in range(MAX_ITER):
            rayVector : RayVector = transitionGenerator.transition()
            if(rayVector is not None):
                rayVectors.append(rayVector)
            else:
                break


        return rayVectors

@dataclass
class TransitionOutput:
    interface : Interface
    rayVector: RayVector | None


class TransitionGenerator:
    def __init__(
        self,
        currentState: RayState,
        timeAndLocation: TimeAndLocation,
        heights_m: list[float],
        indexNs: list[complex],
    ) -> None:
        self.currentState: RayState = currentState
        self.timeAndLocation: TimeAndLocation = timeAndLocation
        self.heights_m: list[float] = heights_m
        self.indexNs: list[complex] = indexNs

    def transition(self) -> Optional[RayVector]:
        transitionOutput : TransitionOutput = self.insideLayerOperations(currentRayState=self.currentState)

        if transitionOutput == None:
            #logger.debug("Done with iterations, jump out of loop")
            return None

        self.currentState: RayState = self.onTheEdgeOperations(
            currentState=self.currentState, interface=transitionOutput.interface
        )

        return transitionOutput.rayVector

    def insideLayerOperations(
        self, currentRayState: RayState
    ) -> Optional[TransitionOutput]:
        # ==========================================================================
        # Inside the Layer
        # ==========================================================================
        lla_p1: LLA_Coord = currentRayState.lla

        if max(self.heights_m) <= lla_p1.altitude_m:
            # exiting the loop
            # logger.debug("Exiting the atmosphere")
            return None

        ecef_p1, sVector_m = RayTracerComputations.generatePositionAndVector(
            currentState=currentRayState
        )

        # ==========================================================================
        # use quadratic equation to determine intersection in ECEF of the next layer based prior intersection and vector
        intersection = self._findNextIntersectPoint(
            currentState=currentRayState, ecef_p1=ecef_p1, sVector_m=sVector_m
        )

        if intersection == None:
            # exiting the loop
            logger.debug("Exiting the atmosphere")
            return None

        # ===================================================================
        # determine index transition
        n_1, n_2 = self._estimateIndexesAtTransition(
            indx=intersection.indx, currentState=currentRayState, newAltitude_m=intersection.newAltitude_m
        )

        rayVector = RayVector(
            rayState=currentRayState,
            sVector_m=sVector_m,
            ecef_p1=ecef_p1,
            ecef_p2=intersection.ecef_p2,
            newAltitude_m=intersection.newAltitude_m,
            n_1=n_1,
        )

        # ===================================================================
        lla_p2 = convertFromECEFtoLLA(ecef=intersection.ecef_p2)
        lla_p2.setAltitude(newAlitude_m=intersection.newAltitude_m)

        # estimate entry angle onto the curved layers
        entryAngle_deg = RayTracerComputations.computeEntryAngle(
            exitElevation=currentRayState.exitElevation_deg,
            ecef_p1=ecef_p1,
            ecef_p2=intersection.ecef_p2,
            lla_p1=lla_p1,
            lla_p2=lla_p2,
        )

        interface = Interface(
            n_1=n_1,
            n_2=n_2,
            entryAngle_deg=entryAngle_deg,
            newAltitude_m=intersection.newAltitude_m,
            intersection_LLA=lla_p2,
        )

        return TransitionOutput(interface=interface,rayVector=rayVector)

    def onTheEdgeOperations(
        self, currentState: RayState, interface: Interface
    ) -> RayState:
        n_1 = interface.n_1
        n_2 = interface.n_2

        entryAngle_deg = interface.entryAngle_deg
        newAltitude_m = interface.newAltitude_m
        lla_p2 = interface.intersection_LLA

        # TODO, determine if refraction is occuring
        if newAltitude_m == 0.0:
            # bounce off ground
            exitAngle_deg = -entryAngle_deg
            # convert to elevation pointing up
            currentState = RayState(
                exitElevation_deg=90.0 - exitAngle_deg,
                exitAzimuth_deg=currentState.exitAzimuth_deg,
                lla=lla_p2,
            )
            logger.debug("bounce off ground: flip direction of ray")
        else:
            f_2 = (
                RayTracerComputations.computeGeocentricRadius(lla_p2)
                + lla_p2.altitude_m
            )
            f_1 = (
                RayTracerComputations.computeGeocentricRadius(currentState.lla)
                + currentState.lla.altitude_m
            )

            # Snell's with ellipsoidal layers
            argument = n_1 * f_1 * math.sin(math.radians(entryAngle_deg)) / (n_2 * f_2)

            if argument.real > 1.0:
                # past critical angle -> reflection
                exitAngle_deg = -entryAngle_deg
                logger.debug("past critical angle -> reflection")
                # convert to elevation pointing down
                currentState = RayState(
                    exitElevation_deg=-90.0 - exitAngle_deg,
                    exitAzimuth_deg=currentState.exitAzimuth_deg,
                    lla=lla_p2,
                )
            else:
                # refraction
                refracAngle_rad = cmath.asin(argument)
                exitAngle_deg = math.degrees(refracAngle_rad.real)

                if refracAngle_rad.imag > 0:
                    logger.info("complex angle present")

                # store into a ray state
                if exitAngle_deg >= 0:
                    # convert to elevation pointing up
                    currentState = RayState(
                        exitElevation_deg=90.0 - exitAngle_deg,
                        exitAzimuth_deg=currentState.exitAzimuth_deg,
                        lla=lla_p2,
                    )
                else:
                    # convert to elevation pointing down
                    currentState = RayState(
                        exitElevation_deg=-90.0 - exitAngle_deg,
                        exitAzimuth_deg=currentState.exitAzimuth_deg,
                        lla=lla_p2,
                    )

        return currentState

    def _findNextIntersectPoint(
        self, currentState: RayState, ecef_p1: ECEF_Coord, sVector_m: ECEF_Coord
    ) -> Optional[IntersectionPoint]:
        lla_p1 = currentState.lla

        if currentState.exitElevation_deg > 0:
            # going up
            indx = next(
                x
                for x, val in enumerate(self.heights_m)
                if val > currentState.lla.altitude_m
            )
        else:
            # going down
            indx = (
                len([x for x in self.heights_m if x < currentState.lla.altitude_m]) - 1
            )

        if len(self.heights_m) <= indx:
            logger.debug("Outside ionosphere")
            return None
        else:
            # layer intersection
            newAltitude_m = self.heights_m[indx]

        # ==========================================================================
        # use quadratic equation to determine intersection in ECEF of the next layer based prior intersection and vector
        try:
            ecef_p2 = RayTracerComputations.computeNewIntersection(
                ecef_m=ecef_p1, sVector_m=sVector_m, newAltitude_m=newAltitude_m
            )
        except IntersectException as inst1:
            # no intersection, which means (a) angle is down and (b) it is skipping over the lower layer; intersect with self
            if lla_p1.altitude_m in self.heights_m:
                newAltitude_m = lla_p1.altitude_m
            else:
                indx = next(
                    x for x, val in enumerate(self.heights_m) if val > lla_p1.altitude_m
                )
                newAltitude_m = self.heights_m[indx]

            try:
                ecef_p2 = RayTracerComputations.computeNewIntersection(
                    ecef_m=ecef_p1, sVector_m=sVector_m, newAltitude_m=newAltitude_m
                )
            except IntersectException as inst2:
                logger.error(inst2.args)
                raise IntersectException("how did we get here?")
   
        return IntersectionPoint(ecef_p2=ecef_p2, newAltitude_m=newAltitude_m, indx=indx)

    def _estimateIndexesAtTransition(
        self, indx: int, newAltitude_m: float, currentState: RayState
    ) -> tuple[complex, complex]:
        lla_p1 = currentState.lla

        if lla_p1.altitude_m in self.heights_m:
            # standard heights
            if newAltitude_m == lla_p1.altitude_m:
                # horizontal transitions
                n_2 = self.indexNs[indx]
                n_1 = self.indexNs[indx - 1]
                logger.debug("horizontal transitions")
            elif newAltitude_m < lla_p1.altitude_m:
                if newAltitude_m == min(self.heights_m):
                    # to ground
                    n_2 = 3.0  # rough estimate
                    n_1 = self.indexNs[indx]
                    logger.debug("bounce off ground")
                else:
                    n_2 = self.indexNs[indx - 1]
                    n_1 = self.indexNs[indx]
                    logger.debug("down transitions")
            elif newAltitude_m > lla_p1.altitude_m:
                n_2 = self.indexNs[indx]
                n_1 = self.indexNs[indx - 1]
                #logger.debug("up transitions")
        else:
            if newAltitude_m < lla_p1.altitude_m:
                if indx == 0:
                    # to ground
                    n_2 = 3.0  # rough estimate
                    n_1 = self.indexNs[indx]
                    logger.debug("bounce off ground")
                else:
                    n_2 = self.indexNs[indx - 1]
                    n_1 = self.indexNs[indx]
                    logger.debug("down transitions")
            elif newAltitude_m > lla_p1.altitude_m:
                n_2 = self.indexNs[indx]
                n_1 = self.indexNs[indx - 1]
                # logger.debug("up transitions")

        return (n_1, n_2)
    