# ====================================================
# https://geospace-code.github.io/pymap3d/index.html
import pymap3d

# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj

from src.bindings.positional.coordinates_class import (
    AER_Coord,
    ECEF_Coord,
    ENU_Coord,
    LLA_Coord,
)

# ====================================================
# constants
ECEF = pyproj.Proj(proj="geocent", ellps="WGS84", datum="WGS84")
LLA = pyproj.Proj(proj="latlong", ellps="WGS84", datum="WGS84")


def convertFromLLAtoECEF(lla: LLA_Coord) -> ECEF_Coord:
    # ECEF location
    x_m, y_m, z_m = pyproj.transform(
        LLA, ECEF, lla.lon_deg, lla.lat_deg, lla.altitude_m, radians=False
    )
    return ECEF_Coord(x_m, y_m, z_m)


def convertFromAER(aer: AER_Coord, lla: LLA_Coord) -> ECEF_Coord:
    ecef = pymap3d.aer2ecef(
        az=aer.az_deg,
        el=aer.ele_deg,
        srange=aer.range_m,
        lat0=lla.lat_deg,
        lon0=lla.lon_deg,
        alt0=lla.altitude_m,
        ell=None,
        deg=True,
    )

    return ecef


def convertFromAER2ENU(aer: AER_Coord) -> ENU_Coord:
    east, north, up = pymap3d.aer2enu(
        az=aer.az_deg, el=aer.ele_deg, srange=aer.range_m, deg=True
    )

    return ENU_Coord(e_m=east, n_m=north, u_m=up)


def convertToAER(ecef: ECEF_Coord, lla: LLA_Coord) -> AER_Coord:
    az_deg, ele_deg, range_m = pymap3d.ecef2aer(
        x=ecef.x_m,
        y=ecef.y_m,
        z=ecef.z_m,
        lat0=lla.lat_deg,
        lon0=lla.lon_deg,
        h0=lla.altitude_m,
        ell=None,
        deg=True,
    )

    return AER_Coord(az_deg=az_deg, ele_deg=ele_deg, range_m=range_m)


def convertFromECEFtoLLA(ecef: ECEF_Coord) -> LLA_Coord:
    lon_deg, lat_deg, alt_m = pyproj.transform(
        ECEF, LLA, ecef.x_m, ecef.y_m, ecef.z_m, radians=False
    )

    return LLA_Coord(lat_deg=lat_deg, lon_deg=lon_deg, altitude_m=alt_m)
