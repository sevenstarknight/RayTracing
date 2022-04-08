## ====================================================
# specialized imports
# https://pypi.org/project/nrlmsise00/
from nrlmsise00 import msise_model

## ====================================================
# local imports
from models.msiseoutput_class import MSISEOuput
from bindings.coordinates_class import LLA
from models.abstractspacephysics_model import AbstractSpacePhysicsModel
from raystate_class import RayState

class MSISE_Model(AbstractSpacePhysicsModel):

    def generatePointEstimate(self,  rayPoint : LLA) ->MSISEOuput:
            #Atmosphere Model
            ds, ts = msise_model(self.currentDateTime, rayPoint.altitude_m/1000, rayPoint.lat_deg, rayPoint.lon_deg, 
            self.ionosphereState.f107a, self.ionosphereState.f107, self.ionosphereState.ap[0])
            return(MSISEOuput(ds,ts))

    def generateSetEstimate(self,  rayPoints : list[LLA]) ->list[MSISEOuput]:

        msiseList = []
        for rayPoint in rayPoints:
            msiseList.append(self.generatePointEstimate(rayPoint))

        return(msiseList)

    def generateSetEstimateFromRayState(self,  rayPoints : list[RayState]) ->list[MSISEOuput]:

        msiseList = []
        for rayPoint in rayPoints:
            msiseList.append(self.generatePointEstimate(rayPoint.lla))

        return(msiseList)