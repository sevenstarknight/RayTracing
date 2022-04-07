# https://pyproj4.github.io/pyproj/stable/
import pyproj
# https://geospace-code.github.io/pymap3d/index.html
import pymap3d
## ====================================================
# local imports
from bindings.coordinates_class import LLA, ECEF
from bindings.timeandlocation_class import TimeAndLocation
from raytracer_computations import generatePositionAndVector, computeSlantIntersections
from raystate_class import RayState
from bindings.ionospherestate_class import IonosphereState
from indexrefractionmodels.xmodel import XModel
from indexrefractionmodels.dispersionmodels_enum import DispersionModel

from models.igrf_model import IGRF_Model
from models.iri_model import IRI_Model
from models.msise_model import MSISE_Model
from models.spacephysicsmodels import SpacePhysicsModels


ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')

class IndexOfRefractionGenerator():

    def __init__(self, frequency_hz : float, dispersionModel : DispersionModel):
        self.frequency_hz = frequency_hz
        self.dispersionModel = dispersionModel

    def estimateSlantPath(self, startTimeAndLocation : TimeAndLocation, sat_ECEF : ECEF, heightStratification_m : list[float]) -> list[RayState]:
        #expected height, assume minimal change in position with range projection, so assume slant path for ionosphere model
        initialAz_deg, initialEle_deg, initialRange_m = pymap3d.ecef2aer(sat_ECEF.x_m, sat_ECEF.y_m, sat_ECEF.z_m,
            startTimeAndLocation.eventLocation_LLA.lat_deg, startTimeAndLocation.eventLocation_LLA.lon_deg, 
            startTimeAndLocation.eventLocation_LLA.altitude_m, ell=None, deg=True)

        rayState = RayState(exitAzimuth_deg=initialAz_deg, exitElevation_deg=initialEle_deg, lla=startTimeAndLocation.eventLocation_LLA, nIndex = 1.0)
        ecef_p1, sVector_m = generatePositionAndVector(rayState)

        intersects_ECEF = computeSlantIntersections(ecef_p1, sVector_m, heightStratification_m)
        # make LLAs
        listOfSlant_RayState = []
        for indx in range(len(intersects_ECEF)):
            intersect_ECEF = intersects_ECEF[indx]
            height = heightStratification_m[indx]

            lon_deg, lat_deg, alt_m = pyproj.transform(ecef, lla, intersect_ECEF.x_m, intersect_ECEF.y_m, intersect_ECEF.z_m, radians=False)
            intersect_LLA = LLA(lat_deg, lon_deg, height) # force to altitude, loss because of approx.

            rayState = RayState(exitAzimuth_deg=initialAz_deg, exitElevation_deg=initialEle_deg, lla=intersect_LLA, nIndex = 1.0)
            listOfSlant_RayState.append(rayState)

        return(listOfSlant_RayState)

    def estimateIndexN(self, startTimeAndLocation : TimeAndLocation, sat_ECEF : ECEF, heightStratification_m : list[float])-> list[complex]:

        # make LLAs
        listOfSlant_RayState = self.estimateSlantPath(startTimeAndLocation, sat_ECEF, heightStratification_m)

        # make the model
        ionosphereState = IonosphereState(10.0, 10.0, 3.0)
        igrf = IGRF_Model(currentDateTime=startTimeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)
        iri = IRI_Model(currentDateTime=startTimeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)
        msise = MSISE_Model(currentDateTime=startTimeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)

        spm = SpacePhysicsModels(igrf=igrf, msise=msise, iri=iri)

        # model the index of refraction
        xModel = XModel(spacePhysicsModels=spm, frequency_hz=self.frequency_hz)

        listIndexN = []
        for rayState in listOfSlant_RayState:
            indexN = xModel.estimateIndexOfRefraction(currentState = rayState)
            listIndexN.append(indexN)

        return(listIndexN)