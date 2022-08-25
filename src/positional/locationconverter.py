# ====================================================
# https://geospace-code.github.io/pymap3d/index.html
import pymap3d

# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj

from src.bindings.coordinates_class import AER_Coord, ECEF_Coord, LLA_Coord
# ====================================================
# constants
ECEF = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
LLA = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


def convertFromLLAtoECEF(lla: LLA_Coord) -> ECEF_Coord:
    # ECEF location
    x_m, y_m, z_m = pyproj.transform(
        LLA, ECEF, lla.lon_deg, lla.lat_deg, lla.altitude_m, radians=False)
    return ECEF_Coord(x_m, y_m, z_m)

def convertFromAER(aer :AER_Coord, lla: LLA_Coord) -> ECEF_Coord:
    ecef = pymap3d.aer2ecef(aer.az_deg, aer.ele_deg, aer.range_m,
                                       lla.lat_deg, lla.lon_deg, lla.altitude_m, ell=None, deg=True)

    return ecef

def convertToAER(ecef: ECEF_Coord, lla: LLA_Coord) -> AER_Coord:
    az_deg, ele_deg, range_m = pymap3d.ecef2aer(ecef.x_m, ecef.y_m, ecef.z_m,
                                                lla.lat_deg, lla.lon_deg,
                                                lla.altitude_m, ell=None, deg=True)

    return AER_Coord(az_deg=az_deg, ele_deg=ele_deg, range_m=range_m)


def convertFromECEFtoLLA(ecef: ECEF_Coord) -> LLA_Coord:

    lon_deg, lat_deg, alt_m = pyproj.transform(
        ECEF, LLA, ecef.x_m, ecef.y_m, ecef.z_m, radians=False)

    return LLA_Coord(lat_deg=lat_deg, lon_deg=lon_deg, altitude_m=alt_m)
