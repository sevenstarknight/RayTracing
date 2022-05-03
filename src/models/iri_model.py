# ====================================================
# https://github.com/space-physics/iri2016
from iri2016 import IRI

# ====================================================
# local imports
from src.models.abstractspacephysics_model import AbstractSpacePhysicsModel
from src.models.irioutput_class import IRIOutput
from src.bindings.coordinates_class import LLA_Coord
from src.raystate_class import RayState

class IRI_Model(AbstractSpacePhysicsModel):

    def generatePointEstimate(self,  rayPoint: LLA_Coord) -> IRIOutput:
        altkmrange = (rayPoint.altitude_m/1000,
                      rayPoint.altitude_m/1000 + 1, 1.0)
        iri = IRI(self.currentDateTime, altkmrange,
                  rayPoint.lat_deg, rayPoint.lat_deg)
        return(IRIOutput(iri))

    def generateSetEstimate(self,  rayPoints: list[LLA_Coord]) -> list[IRIOutput]:
        iriOutputs = []
        for rayPoint in rayPoints:
            iriOutputs.append(self.generatePointEstimate(rayPoint))

        return(iriOutputs)

    def generateSetEstimateFromRayState(self,  rayPoints: list[RayState]) -> list[IRIOutput]:
        iriOutputs = []
        for rayPoint in rayPoints:
            iriOutputs.append(self.generatePointEstimate(rayPoint.lla))

        return(iriOutputs)
