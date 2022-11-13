
# ====================================================
# local imports
from src.bindings.positional.coordinates_class import LLA_Coord, ECEF_Coord
from src.bindings.positional.timeandlocation_class import TimeAndLocation
from src.bindings.positional.layer_class import Layer
from src.bindings.raytracer.raystate_class import RayState
from src.positional.locationconverter_computations import convertFromECEFtoLLA, convertToAER
from src.raytracer.raytracer_computations import RayTracerComputations



class SlantPathGenerator():

    def estimateSlantPath(self, startTimeAndLocation: TimeAndLocation, sat_ECEF: ECEF_Coord, 
    heightStratification_m: list[float]) -> list[Layer]:

        aer = convertToAER(
            ecef=sat_ECEF, lla=startTimeAndLocation.eventLocation_LLA)

        rayState = RayState(exitAzimuth_deg=aer.az_deg, exitElevation_deg=aer.ele_deg,
                            lla=startTimeAndLocation.eventLocation_LLA)

        ecef_p1, sVector_m = RayTracerComputations.generatePositionAndVector(rayState)

        intersects_ECEF: list[ECEF_Coord] = RayTracerComputations.computeSlantIntersections(
            ecef_p1, sVector_m, heightStratification_m)
            
        # make LLAs
        layers = []
        for indx in range(len(intersects_ECEF)):
            ecef_p2 = intersects_ECEF[indx]
            height = heightStratification_m[indx]

            lla_p1 : LLA_Coord = convertFromECEFtoLLA(ecef=ecef_p1)

            layer = Layer(ecef_p1=ecef_p1, ecef_p2 = ecef_p2, newAltitude_m=height, lla = lla_p1, aer = aer)
            layers.append(layer)
            
            ecef_p1 = ecef_p2

        return(layers)
