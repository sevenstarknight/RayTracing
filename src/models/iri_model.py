# ====================================================
# https://github.com/space-physics/iri2016
from iri2016 import IRI

# ====================================================
# local imports
from models.abstractspacephysics_model import AbstractSpacePhysicsModel
from models.irioutput_class import IRIOutput
from bindings.coordinates_class import LLA
from raystate_class import RayState

class IRI_Model(AbstractSpacePhysicsModel):

    def generatePointEstimate(self,  rayPoint: LLA) -> IRIOutput:
        altkmrange = (rayPoint.altitude_m/1000,
                      rayPoint.altitude_m/1000 + 1, 1.0)
        iri = IRI(self.currentDateTime, altkmrange,
                  rayPoint.lat_deg, rayPoint.lat_deg)
        return(IRIOutput(iri))

    def generateSetEstimate(self,  rayPoints: list[LLA]) -> list[IRIOutput]:
        iriOutputs = []
        for rayPoint in rayPoints:
            iriOutputs.append(self.generatePointEstimate(rayPoint))

        return(iriOutputs)

    def generateSetEstimateFromRayState(self,  rayPoints: list[RayState]) -> list[IRIOutput]:
        iriOutputs = []
        for rayPoint in rayPoints:
            iriOutputs.append(self.generatePointEstimate(rayPoint.lla))

        return(iriOutputs)
