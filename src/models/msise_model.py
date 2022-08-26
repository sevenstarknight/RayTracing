# ====================================================
# https://pypi.org/project/nrlmsise00/
from nrlmsise00 import msise_model

# ====================================================
# local imports
from src.models.abstractspacephysics_model import AbstractSpacePhysicsModel
from src.models.msiseoutput_class import MSISEOutput
from src.bindings.coordinates_class import LLA_Coord
from src.raystate_class import RayState
from src.rayvector_class import RayVector


class MSISE_Model(AbstractSpacePhysicsModel):

    def generatePointEstimate(self,  rayPoint: RayVector) -> MSISEOutput:
        # Atmosphere Model
        ds, ts = msise_model(time=self.currentDateTime, alt=rayPoint.altitude_m/1000, lat=rayPoint.lat_deg, lon=rayPoint.lon_deg,
                             f107a=self.ionosphereState.f107a, f107=self.ionosphereState.f107, ap=self.ionosphereState.ap[0], ap_a=self.ionosphereState.ap)
        return(MSISEOutput(ds, ts))

    def generateSetEstimate(self,  rayPoints: list[LLA_Coord]) -> list[MSISEOutput]:

        msiseOutputs = []
        for rayPoint in rayPoints:
            msiseOutputs.append(self.generatePointEstimate(rayPoint))

        return(msiseOutputs)

    def generateSetEstimateFromRayState(self,  rayPoints: list[RayState]) -> list[MSISEOutput]:

        msiseOutputs = []
        for rayPoint in rayPoints:
            msiseOutputs.append(self.generatePointEstimate(rayPoint.lla))

        return(msiseOutputs)
