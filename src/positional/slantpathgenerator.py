
# ====================================================
# local imports
from src.bindings.coordinates_class import LLA_Coord, ECEF_Coord
from src.bindings.timeandlocation_class import TimeAndLocation
from src.positional.locationconverter import convertFromECEFtoLLA, convertToAER
from src.raytracer.raytracer_computations import generatePositionAndVector, computeSlantIntersections
from src.raystate_class import RayState


class SlantPathGenerator():

    def estimateSlantPath(self, startTimeAndLocation: TimeAndLocation, sat_ECEF: ECEF_Coord, heightStratification_m: list[float]) -> list[RayState]:

        aer = convertToAER(
            ecef=sat_ECEF, lla=startTimeAndLocation.eventLocation_LLA)

        rayState = RayState(exitAzimuth_deg=aer.az_deg, exitElevation_deg=aer.ele_deg,
                            lla=startTimeAndLocation.eventLocation_LLA, nIndex=1.0)
        ecef_p1, sVector_m = generatePositionAndVector(rayState)

        intersects_ECEF = computeSlantIntersections(
            ecef_p1, sVector_m, heightStratification_m)
            
        # make LLAs
        slantRayStates = []
        for indx in range(len(intersects_ECEF)):
            intersect_ECEF = intersects_ECEF[indx]
            height = heightStratification_m[indx]

            intersect_LLA : LLA_Coord = convertFromECEFtoLLA(ecef=intersect_ECEF)
            # force to altitude, loss because of approx.
            intersect_LLA.setAltitude(newAlitude_m=height)

            rayState = RayState(exitAzimuth_deg=aer.az_deg,
                                exitElevation_deg=aer.ele_deg, lla=intersect_LLA, nIndex=1.0)
            slantRayStates.append(rayState)

        return(slantRayStates)
