## ====================================================
# specialized imports
#https://github.com/space-physics/wmm2020
import igrf

## ====================================================
# local imports
from models.abstractspacephysics_model import AbstractSpacePhysicsModel
from bindings.coordinates_class import LLA
from models.igrfoutput_class import IGRFOutput
from raystate_class import RayState

class IGRF_Model(AbstractSpacePhysicsModel):
    
    def generatePointEstimate(self,  rayPoint : LLA) ->IGRFOutput:
        mag = igrf.igrf(self.currentDateTime, glat=rayPoint.lat_deg, glon=rayPoint.lon_deg, alt_km=rayPoint.altitude_m/1000.0)
        return(IGRFOutput(mag))

    def generateSetEstimate(self,  rayPoints : list[LLA]) ->list[IGRFOutput]:
        igrfList = []
        for rayPoint in rayPoints:
            igrfList.append(self.generatePointEstimate(rayPoint))

        return(igrfList)

    def generateSetEstimateFromRayState(self,  rayPoints : list[RayState]) ->list[IGRFOutput]:
        igrfList = []
        for rayPoint in rayPoints:
            igrfList.append(self.generatePointEstimate(rayPoint.lla))

        return(igrfList)