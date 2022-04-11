# ====================================================
import math

# ====================================================
# https://ahrs.readthedocs.io/en/latest/wgs84.html
import ahrs
# https://pyproj4.github.io/pyproj/stable/
import pyproj
# https://geospace-code.github.io/pymap3d/index.html
import pymap3d

# ====================================================
# local imports
from bindings.exceptions_class import IntersectException
from bindings.coordinates_class import LLA, ECEF
from raystate_class import RayState

ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


def computeGeocentricRadius(lla: LLA) -> float:
    # Estimates the geocentric radius given the input LLA (geo distance)
    wgs = ahrs.utils.WGS()

    lat_rad = math.radians(lla.lat_deg)

    aXCosSq_mSq = (wgs.a*math.cos(lat_rad))*(wgs.a*math.cos(lat_rad))
    bXSinSq_mSq = (wgs.b*math.sin(lat_rad))*(wgs.b*math.sin(lat_rad))

    num = wgs.a*wgs.a*aXCosSq_mSq + wgs.b*wgs.b*bXSinSq_mSq
    denom = aXCosSq_mSq + bXSinSq_mSq

    return(math.sqrt(num/denom))


def generatePositionAndVector(currentState: RayState) -> ECEF:
    lla_p1 = currentState.lla

    # ECEF location
    x_m, y_m, z_m = pyproj.transform(
        lla, ecef, lla_p1.lon_deg, lla_p1.lat_deg, lla_p1.altitude_m, radians=False)
    ecef_p1 = ECEF(x_m, y_m, z_m)

    # Generate ECEF Vector Based on Ray Direction using AER
    ecef_unitVector = pymap3d.aer2ecef(currentState.exitAzimuth_deg, currentState.exitElevation_deg, 1.0,
                                       lla_p1.lat_deg, lla_p1.lon_deg, lla_p1.altitude_m, ell=None, deg=True)
    ecef_unit = ECEF(ecef_unitVector[0],
                     ecef_unitVector[1], ecef_unitVector[2])

    sVector_m = ECEF.subtract(ecef_p1, ecef_unit)

    return(ecef_p1, sVector_m)


def computeSlantIntersections(ecef_m: ECEF, sVector_m: float, newAltitudes_m: list[float]) -> list[ECEF]:

    intersections_ECEF = []
    for newAltitude_m in newAltitudes_m:
        intersection_ECEF = computeNewIntersection(
            ecef_m, sVector_m, newAltitude_m)
        intersections_ECEF.append(intersection_ECEF)

    return(intersections_ECEF)


def computeNewIntersection(ecef_m: ECEF, sVector_m: float, newAltitude_m: float) -> ECEF:
    # find the new intersection between the ECEF, the vector, and the new altitude
    # fails and throws exception if intersection doesn't occur
    wgs = ahrs.utils.WGS()

    d = sVector_m.x_m*sVector_m.x_m/(wgs.a + newAltitude_m)**2 + \
        sVector_m.y_m*sVector_m.y_m/(wgs.a + newAltitude_m)**2 + \
        sVector_m.z_m*sVector_m.z_m/(wgs.b + newAltitude_m)**2

    e = 2.0*(ecef_m.x_m*sVector_m.x_m/(wgs.a + newAltitude_m)**2 +
             ecef_m.y_m*sVector_m.y_m/(wgs.a + newAltitude_m)**2 +
             ecef_m.z_m*sVector_m.z_m/(wgs.b + newAltitude_m)**2)

    f = ecef_m.x_m*ecef_m.x_m/(wgs.a + newAltitude_m)**2 + \
        ecef_m.y_m*ecef_m.y_m/(wgs.a + newAltitude_m)**2 + \
        ecef_m.z_m*ecef_m.z_m/(wgs.b + newAltitude_m)**2 - 1

    radical = e*e - 4*d*f
    if radical > 0.0:
        t = (-e + math.sqrt(radical))/(2*d)

        xprime = ecef_m.x_m + t*sVector_m.x_m
        yprime = ecef_m.y_m + t*sVector_m.y_m
        zprime = ecef_m.z_m + t*sVector_m.z_m

        return(ECEF(xprime, yprime, zprime))
    else:
        raise IntersectException("No Intersection with Layer")


def computeEntryAngle(exitElevation: float, ecef_p1: ECEF, ecef_p2: ECEF, lla_p1: LLA, lla_p2: LLA) -> float:
    # Compute the entry angle to the next layer based on the ray and the curved surface for the layers
    s12 = ECEF.subtract(ecef_p2, ecef_p1).magnitude()
    f_2 = computeGeocentricRadius(lla_p2) + lla_p2.altitude_m
    f_1 = computeGeocentricRadius(lla_p1) + lla_p1.altitude_m

    num = -f_1*f_1 + f_2*f_2 + s12*s12
    denom = 2*f_2*s12
    ratio = num/denom

    if(ratio > 1.0):
        angle = 0
    else:
        angle = math.degrees(math.acos(ratio))

    if(exitElevation > 0):
        entryAngle = angle
    else:
        if(math.fabs(lla_p1.altitude_m - lla_p2.altitude_m) < 1e-4):
            entryAngle = angle
        else:
            entryAngle = -(90 - angle)

    return(entryAngle)
