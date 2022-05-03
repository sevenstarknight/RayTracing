# ====================================================
# https://github.com/space-physics/wmm2020
import igrf

# ====================================================
# local imports
from src.models.abstractspacephysics_model import AbstractSpacePhysicsModel
from src.models.igrfoutput_class import IGRFOutput
from src.bindings.coordinates_class import LLA_Coord
from src.raystate_class import RayState


class IGRF_Model(AbstractSpacePhysicsModel):

    def generatePointEstimate(self,  rayPoint: LLA_Coord) -> IGRFOutput:
        mag = igrf.igrf(self.currentDateTime, glat=rayPoint.lat_deg,
                        glon=rayPoint.lon_deg, alt_km=rayPoint.altitude_m/1000.0)
        return(IGRFOutput(mag))

    def generateSetEstimate(self,  rayPoints: list[LLA_Coord]) -> list[IGRFOutput]:
        igrfOutputs = []
        for rayPoint in rayPoints:
            igrfOutputs.append(self.generatePointEstimate(rayPoint))

        return(igrfOutputs)

    def generateSetEstimateFromRayState(self,  rayPoints: list[RayState]) -> list[IGRFOutput]:
        igrfOutputs = []
        for rayPoint in rayPoints:
            igrfOutputs.append(self.generatePointEstimate(rayPoint.lla))

        return(igrfOutputs)
