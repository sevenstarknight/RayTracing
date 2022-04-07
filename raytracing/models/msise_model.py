## ====================================================
# specialized imports
# https://pypi.org/project/nrlmsise00/
from nrlmsise00 import msise_model

## ====================================================
# local imports
from models.msiseoutput_class import MSISE
from bindings.coordinates_class import LLA
from models.abstractspacephysics_model import AbstractSpacePhysicsModel
from raystate_class import RayState

class MSISE_Model(AbstractSpacePhysicsModel):

    def generatePointEstimate(self,  rayPoint : LLA) ->MSISE:
            #Atmosphere Model
            ds, ts = msise_model(self.currentDateTime, rayPoint.altitude_m/1000, rayPoint.lat_deg, rayPoint.lon_deg, 
            self.ionosphereState.f107a, self.ionosphereState.f107, self.ionosphereState.ap[0])
            return(MSISE(ds,ts))

    def generateSetEstimate(self,  rayPoints : list[LLA]) ->list[MSISE]:

        msiseList = []
        for rayPoint in rayPoints:
            msiseList.append(self.generatePointEstimate(rayPoint))

        return(msiseList)

    def generateSetEstimateFromRayState(self,  rayPoints : list[RayState]) ->list[MSISE]:

        msiseList = []
        for rayPoint in rayPoints:
            msiseList.append(self.generatePointEstimate(rayPoint.lla))

        return(msiseList)