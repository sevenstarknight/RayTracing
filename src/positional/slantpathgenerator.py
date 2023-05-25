# ====================================================
# local imports
from src.bindings.positional.coordinates_class import AER_Coord, LLA_Coord, ECEF_Coord
from src.bindings.positional.timeandlocation_class import TimeAndLocation
from src.bindings.positional.layer_class import Layer
from src.bindings.raytracer.raystate_class import RayState
from src.positional.locationconverter_computations import (
    convertFromECEFtoLLA,
    convertToAER,
)
from src.raytracer.raytracer_computations import RayTracerComputations


class SlantPathGenerator:
    def estimateSlantPath(
        self,
        startTimeAndLocation: TimeAndLocation,
        sat_ECEF: ECEF_Coord,
        heightStratification_m: list[float],
    ) -> list[Layer]:
        aer: AER_Coord = convertToAER(
            ecef=sat_ECEF, lla=startTimeAndLocation.eventLocation_LLA
        )

        rayState = RayState(
            exitAzimuth_deg=aer.az_deg,
            exitElevation_deg=aer.ele_deg,
            lla=startTimeAndLocation.eventLocation_LLA,
        )

        ecef_p1, sVector_m = RayTracerComputations.generatePositionAndVector(
            currentState=rayState
        )

        intersects_ECEF: list[ECEF_Coord] = RayTracerComputations.computeSlantIntersections(
            ecef_m=ecef_p1, sVector_m=sVector_m, newAltitudes_m=heightStratification_m
        )

        # construct the builder
        layerBuilder = LayerBuilder(
            intersects_ECEF=intersects_ECEF,
            heightStratification_m=heightStratification_m,
            ecef_p1=ecef_p1,
            aer=aer,
        )

        # make layers (in LLA)
        layers = [layerBuilder.build(indx) for indx in range(len(intersects_ECEF))]

        return layers


class LayerBuilder:
    def __init__(
        self,
        intersects_ECEF: list[ECEF_Coord],
        heightStratification_m: list[float],
        aer: AER_Coord,
        ecef_p1: ECEF_Coord,
    ) -> None:
        self.intersects_ECEF = intersects_ECEF
        self.heightStratification_m = heightStratification_m
        self.aer = aer
        self.ecef_p1 = ecef_p1

    def build(self, indx: int) -> Layer:
        ecef_p2: ECEF_Coord = self.intersects_ECEF[indx]
        bottomAltitude = self.heightStratification_m[indx]

        lla_p1: LLA_Coord = convertFromECEFtoLLA(ecef=self.ecef_p1)
        lla_p2: LLA_Coord = convertFromECEFtoLLA(ecef=ecef_p2)

        layer = Layer(
            ecef_p1=self.ecef_p1,
            ecef_p2=ecef_p2,
            lla_p1=lla_p1,
            lla_p2=lla_p2,
            aer=self.aer,
        )

        # replace in memory
        self.ecef_p1: ECEF_Coord = ecef_p2

        return layer
