# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj
# https://geospace-code.github.io/pymap3d/index.html
import pymap3d
# ====================================================
# local imports
from src.bindings.coordinates_class import LLA, ECEF
from src.bindings.timeandlocation_class import TimeAndLocation
from src.raytracer_computations import generatePositionAndVector, computeSlantIntersections
from src.raystate_class import RayState
# ====================================================
# constants
ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


class SlantPathGenerator():

    def estimateSlantPath(self, startTimeAndLocation: TimeAndLocation, sat_ECEF: ECEF, heightStratification_m: list[float]) -> list[RayState]:
        # expected height, assume minimal change in position with range projection, so assume slant path for ionosphere model
        initialAz_deg, initialEle_deg, initialRange_m = pymap3d.ecef2aer(sat_ECEF.x_m, sat_ECEF.y_m, sat_ECEF.z_m,
                                                                         startTimeAndLocation.eventLocation_LLA.lat_deg, startTimeAndLocation.eventLocation_LLA.lon_deg,
                                                                         startTimeAndLocation.eventLocation_LLA.altitude_m, ell=None, deg=True)

        rayState = RayState(exitAzimuth_deg=initialAz_deg, exitElevation_deg=initialEle_deg,
                            lla=startTimeAndLocation.eventLocation_LLA, nIndex=1.0)
        ecef_p1, sVector_m = generatePositionAndVector(rayState)

        intersects_ECEF = computeSlantIntersections(
            ecef_p1, sVector_m, heightStratification_m)
        # make LLAs
        slantRayStates = []
        for indx in range(len(intersects_ECEF)):
            intersect_ECEF = intersects_ECEF[indx]
            height = heightStratification_m[indx]

            lon_deg, lat_deg, alt_m = pyproj.transform(
                ecef, lla, intersect_ECEF.x_m, intersect_ECEF.y_m, intersect_ECEF.z_m, radians=False)
            # force to altitude, loss because of approx.
            intersect_LLA = LLA(lat_deg, lon_deg, height)

            rayState = RayState(exitAzimuth_deg=initialAz_deg,
                                exitElevation_deg=initialEle_deg, lla=intersect_LLA, nIndex=1.0)
            slantRayStates.append(rayState)

        return(slantRayStates)
