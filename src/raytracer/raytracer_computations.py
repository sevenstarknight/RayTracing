import math

# ====================================================
# https://ahrs.readthedocs.io/en/latest/wgs84.html
import ahrs

# ====================================================
# local imports
from src.bindings.exceptions_class import IntersectException
from src.bindings.positional.coordinates_class import AER_Coord, LLA_Coord, ECEF_Coord
from src.bindings.raytracer.raystate_class import RayState
from src.positional.locationconverter_computations import LocationConverterComputation


class RayTracerComputations:
    @staticmethod
    def computeGeocentricRadius(lla: LLA_Coord) -> float:
        # Estimates the geocentric radius given the input LLA (geo distance)
        wgs = ahrs.utils.WGS()

        lat_rad = math.radians(lla.lat_deg)

        aXCosSq_mSq = (wgs.a * math.cos(lat_rad)) * (wgs.a * math.cos(lat_rad))
        bXSinSq_mSq = (wgs.b * math.sin(lat_rad)) * (wgs.b * math.sin(lat_rad))

        num = wgs.a * wgs.a * aXCosSq_mSq + wgs.b * wgs.b * bXSinSq_mSq
        denom = aXCosSq_mSq + bXSinSq_mSq

        return math.sqrt(num / denom)

    @staticmethod
    def generatePositionAndVector(
        currentState: RayState,
    ) -> tuple[ECEF_Coord, ECEF_Coord]:
        lla_p1 = currentState.lla

        # ECEF location
        ecef_p1 = LocationConverterComputation.convertFromLLAtoECEF(lla_p1)

        # Generate ECEF Vector Based on Ray Direction using AER
        aer = AER_Coord(
            currentState.exitAzimuth_deg, currentState.exitElevation_deg, 1.0
        )
        ecef_unitVector = LocationConverterComputation.convertFromAER(aer=aer, lla=lla_p1)

        ecef_unit = ECEF_Coord(
            ecef_unitVector[0], ecef_unitVector[1], ecef_unitVector[2]
        )

        sVector_m = ECEF_Coord.subtract(ecef_p1, ecef_unit)

        return (ecef_p1, sVector_m)

    @staticmethod
    def computeSlantIntersections(
        ecef_m: ECEF_Coord, sVector_m: ECEF_Coord, newAltitudes_m: list[float]
    ) -> list[ECEF_Coord]:
        intersections_ECEF = [
            RayTracerComputations.computeNewIntersection(
                ecef_m=ecef_m, sVector_m=sVector_m, newAltitude_m=newAltitude_m
            )
            for newAltitude_m in newAltitudes_m
        ]

        return intersections_ECEF

    @staticmethod
    def computeNewIntersection(
        ecef_m: ECEF_Coord, sVector_m: ECEF_Coord, newAltitude_m: float
    ) -> ECEF_Coord:
        # find the new intersection between the ECEF, the vector, and the new altitude
        # fails and throws exception if intersection doesn't occur
        wgs = ahrs.utils.WGS()

        d = (
            sVector_m.x_m * sVector_m.x_m / (wgs.a + newAltitude_m) ** 2
            + sVector_m.y_m * sVector_m.y_m / (wgs.a + newAltitude_m) ** 2
            + sVector_m.z_m * sVector_m.z_m / (wgs.b + newAltitude_m) ** 2
        )

        e = 2.0 * (
            ecef_m.x_m * sVector_m.x_m / (wgs.a + newAltitude_m) ** 2
            + ecef_m.y_m * sVector_m.y_m / (wgs.a + newAltitude_m) ** 2
            + ecef_m.z_m * sVector_m.z_m / (wgs.b + newAltitude_m) ** 2
        )

        f = (
            ecef_m.x_m * ecef_m.x_m / (wgs.a + newAltitude_m) ** 2
            + ecef_m.y_m * ecef_m.y_m / (wgs.a + newAltitude_m) ** 2
            + ecef_m.z_m * ecef_m.z_m / (wgs.b + newAltitude_m) ** 2
            - 1
        )

        radical = e * e - 4 * d * f
        if radical > 0.0:
            t = (-e + math.sqrt(radical)) / (2 * d)

            xprime = ecef_m.x_m + t * sVector_m.x_m
            yprime = ecef_m.y_m + t * sVector_m.y_m
            zprime = ecef_m.z_m + t * sVector_m.z_m

            return ECEF_Coord(x_m=xprime, y_m=yprime, z_m=zprime)
        else:
            raise IntersectException("No Intersection with Layer")

    @staticmethod
    def computeEntryAngle(
        exitElevation: float,
        ecef_p1: ECEF_Coord,
        ecef_p2: ECEF_Coord,
        lla_p1: LLA_Coord,
        lla_p2: LLA_Coord,
    ) -> float:
        # Compute the entry angle to the next layer based on the ray and the curved surface for the layers
        s12 = ECEF_Coord.subtract(ecef1=ecef_p2, ecef2=ecef_p1).magnitude()
        f_2 = (
            RayTracerComputations.computeGeocentricRadius(lla=lla_p2)
            + lla_p2.altitude_m
        )
        f_1 = (
            RayTracerComputations.computeGeocentricRadius(lla=lla_p1)
            + lla_p1.altitude_m
        )

        num = -f_1 * f_1 + f_2 * f_2 + s12 * s12
        denom = 2 * f_2 * s12
        ratio = num / denom

        if ratio > 1.0:
            angle = 0
        else:
            angle = math.degrees(math.acos(ratio))

        if exitElevation > 0:
            entryAngle = angle
        else:
            if math.fabs(lla_p1.altitude_m - lla_p2.altitude_m) < 1e-4:
                entryAngle = angle
            else:
                entryAngle = -(90 - angle)

        return entryAngle
