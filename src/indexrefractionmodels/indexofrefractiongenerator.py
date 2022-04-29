# ====================================================
# local imports
from src.bindings.coordinates_class import ECEF
from src.bindings.timeandlocation_class import TimeAndLocation
from src.raytracer_computations import generatePositionAndVector, computeSlantIntersections
from src.bindings.ionospherestate_class import IonosphereState
from src.indexrefractionmodels.xmodel import XModel
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel

from src.models.igrf_model import IGRF_Model
from src.models.iri_model import IRI_Model
from src.models.msise_model import MSISE_Model
from src.models.spacephysicsmodels import SpacePhysicsModels
from src.positional.slantpathgenerator import SlantPathGenerator


class IndexOfRefractionGenerator():

    def __init__(self, frequency_hz: float, dispersionModel: DispersionModel):
        self.frequency_hz = frequency_hz
        self.dispersionModel = dispersionModel

    def estimateIndexN(self, startTimeAndLocation: TimeAndLocation, sat_ECEF: ECEF, heightStratification_m: list[float]) -> list[complex]:

        slantPathGenerator = SlantPathGenerator()
        # make LLAs
        slantRayStates = slantPathGenerator.estimateSlantPath(
            startTimeAndLocation, sat_ECEF, heightStratification_m)

        # make the model
        ionosphereState = IonosphereState(10.0, 10.0, 3.0)
        igrf = IGRF_Model(
            currentDateTime=startTimeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)
        iri = IRI_Model(currentDateTime=startTimeAndLocation.eventTime_UTC,
                        ionosphereState=ionosphereState)
        msise = MSISE_Model(
            currentDateTime=startTimeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)

        spm = SpacePhysicsModels(igrf=igrf, msise=msise, iri=iri)

        # model the index of refraction
        xModel = XModel(spacePhysicsModels=spm, frequency_hz=self.frequency_hz)

        indexNs = []
        for rayState in slantRayStates:
            indexN = xModel.estimateIndexOfRefraction(currentState=rayState)
            indexNs.append(indexN)

        return(indexNs)
