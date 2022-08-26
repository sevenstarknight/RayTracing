# ====================================================
# https://github.com/space-physics/wmm2020
import igrf

# ====================================================
# local imports
from src.models.abstractspacephysics_model import AbstractSpacePhysicsModel
from src.models.igrfoutput_class import IGRFOutput
from src.rayvector_class import RayVector


class IGRF_Model(AbstractSpacePhysicsModel):

    def generatePointEstimate(self,  rayVector: RayVector) -> IGRFOutput:
        lla = rayVector._rayState.lla
        mag = igrf.igrf(self.currentDateTime, glat=lla.lat_deg,
                        glon=lla.lon_deg, alt_km=lla.altitude_m/1000.0)
        return(IGRFOutput(mag))

    def generateSetEstimate(self,  rayVectors: list[RayVector]) -> list[IGRFOutput]:
        igrfOutputs = []
        for rayVector in rayVectors:
            igrfOutputs.append(self.generatePointEstimate(rayVector))

        return(igrfOutputs)

