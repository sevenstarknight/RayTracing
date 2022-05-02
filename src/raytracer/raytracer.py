import math
import logging
import cmath
# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj

# ====================================================
# local imports
from src.raystate_class import RayState
from src.raytracer.raytracer_computations import computeGeocentricRadius, computeNewIntersection, computeEntryAngle, generatePositionAndVector

from src.raytracer.layeroutput_class import LayerOutput

from src.bindings.exceptions_class import IntersectException
from src.bindings.coordinates_class import LLA
from src.bindings.timeandlocation_class import TimeAndLocation

# ====================================================
# constants
ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
logger = logging.getLogger("mylogger")


class RayTracer():
    def __init__(self, timeAndLocation: TimeAndLocation):
        self.timeAndLocation = timeAndLocation

    def execute(self, heights_m: list[float], indexN: list[complex], params: list[float]) -> list[RayState]:
        '''
        The ray tracer logic, handles the loop that iterates the ray through layers, 
        inputs are the heights of the layers, the associated index of refraction, and 
        the initial exit state of the ray
        '''
        az, el = params
        mod = az % 360
        if(az < 0 or az > 360):
            logger.warn("Round")
            print(mod)

        # =======================================================
        # Initialize the ray state for the start point
        res = next(x for x, val in enumerate(heights_m) if val >=
                   self.timeAndLocation.eventLocation_LLA.altitude_m)

        n_current = indexN[res]

        currentState = RayState(
            el, az, self.timeAndLocation.eventLocation_LLA, n_current)

        # =================================================================
        states = []
        states.append(currentState)

        for idx in range(100):

            layerOutput = self.insideLayerOperations(
                currentState, heights_m, indexN, states)

            if(layerOutput.n_1 == None):
                logger.debug("Done with iterations, jump out of loop")
                states = layerOutput.stateList
                break

            currentState = self.onTheEdgeOperations(currentState, layerOutput)

            states.append(currentState)

        return(states)

    def insideLayerOperations(self, currentState: RayState, heights_m: list[float], indexN: list[complex], stateList: list[RayState]) -> LayerOutput:
        # ==========================================================================
        # Inside the Layer
        # ==========================================================================
        lla_p1 = currentState.lla

        ecef_p1, sVector_m = generatePositionAndVector(currentState)

        if(max(heights_m) <= lla_p1.altitude_m):
            # exiting the loop
            layerOutput = LayerOutput(
                None, None, None, None, None, stateList=stateList)
            logger.debug("Exiting the atmopshere")
            return(layerOutput)

        # ==========================================================================
        # find next layer
        if(currentState.exitElevation_deg > 0):
            # going up
            res = next(x for x, val in enumerate(
                heights_m) if val > lla_p1.altitude_m)

            if(len(heights_m) <= res):
                # exiting the loop
                layerOutput = LayerOutput(
                    None, None, None, None, None, stateList=stateList)
                logger.debug("Exiting the atmopshere")
                return(layerOutput)
            else:
                # layer intersection
                newAltitude_m = heights_m[res]
        else:
            # going down
            res = len([x for x in heights_m if x < lla_p1.altitude_m]) - 1
            newAltitude_m = heights_m[res]

        # ==========================================================================
        # use quadratic equation to determine intersection in ECEF of the next layer based prior intersection and vector
        try:
            ecef_p2 = computeNewIntersection(ecef_p1, sVector_m, newAltitude_m)
        except IntersectException as inst1:
            # no intersection, which means (a) angle is down and (b) it is skipping over the lower layer; intersect with self
            if(lla_p1.altitude_m in heights_m):
                newAltitude_m = lla_p1.altitude_m
            else:
                res = next(x for x, val in enumerate(
                    heights_m) if val > lla_p1.altitude_m)
                newAltitude_m = heights_m[res]

            try:
                ecef_p2 = computeNewIntersection(
                    ecef_p1, sVector_m, newAltitude_m)
            except IntersectException as inst2:
                logger.error(inst2.args)

        # ===================================================================
        # determine index transition
        indx = heights_m.index(newAltitude_m)

        if(lla_p1.altitude_m in heights_m):
            # standard heights
            if(newAltitude_m == lla_p1.altitude_m):
                # horizontal transitions
                n_2 = indexN[indx]
                n_1 = indexN[indx - 1]
                logger.debug("horizontal transitions")
            elif(newAltitude_m < lla_p1.altitude_m):
                if(newAltitude_m == min(heights_m)):
                    # to ground
                    n_2 = 3.0  # rough estimate
                    n_1 = indexN[indx]
                    logger.debug("bounce off ground")
                else:
                    n_2 = indexN[indx - 1]
                    n_1 = indexN[indx]
                    logger.debug("down transitions")
            elif(newAltitude_m > lla_p1.altitude_m):
                n_2 = indexN[indx]
                n_1 = indexN[indx - 1]
                logger.debug("up transitions")
        else:
            if(newAltitude_m < lla_p1.altitude_m):
                if(res == 0):
                    # to ground
                    n_2 = 3.0  # rough estimate
                    n_1 = currentState.nIndex
                    logger.debug("bounce off ground")
                else:
                    n_2 = indexN[indx - 1]
                    n_1 = currentState.nIndex
                    logger.debug("down transitions")
            elif(newAltitude_m > lla_p1.altitude_m):
                n_2 = indexN[indx]
                n_1 = currentState.nIndex
                logger.debug("up transitions")
        # ===================================================================
        lon_deg, lat_deg, alt_m = pyproj.transform(
            ecef, lla, ecef_p2.x_m, ecef_p2.y_m, ecef_p2.z_m, radians=False)
        # force to altitude, loss because of approx.
        lla_p2 = LLA(lat_deg, lon_deg, newAltitude_m)

        # estimate entry angle onto the curved layers
        entryAngle_deg = computeEntryAngle(
            currentState.exitElevation_deg, ecef_p1, ecef_p2, lla_p1, lla_p2)

        layerOutput = LayerOutput(
            n_1, n_2, entryAngle_deg, newAltitude_m, lla_p2, stateList)

        return(layerOutput)

    def onTheEdgeOperations(self, currentState: RayState, layerOutput: LayerOutput) -> RayState:
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
            logger.debug("bounce off ground: flip direction of ray")
        else:
            f_2 = computeGeocentricRadius(lla_p2) + lla_p2.altitude_m
            f_1 = computeGeocentricRadius(
                currentState.lla) + currentState.lla.altitude_m

            # Snell's with ellipsoidal layers
            argument = n_1*f_1*math.sin(math.radians(entryAngle_deg))/(n_2*f_2)

            if(argument.real > 1.0):
                # past critical angle -> reflection
                exitAngle_deg = -entryAngle_deg
                logger.debug("past critical angle -> reflection")
                # convert to elevation pointing down
                currentState = RayState(-90.0 - exitAngle_deg,
                                        currentState.exitAzimuth_deg, lla_p2, n_1)
            else:
                # refraction
                refracAngle_rad = cmath.asin(argument)
                exitAngle_deg = math.degrees(refracAngle_rad.real)

                if(refracAngle_rad.imag > 0):
                    logger.info("complex angle present")

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
