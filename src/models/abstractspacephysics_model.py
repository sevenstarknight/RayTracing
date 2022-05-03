from abc import ABC, abstractmethod
from datetime import datetime

## ====================================================
# local imports
from src.bindings.ionospherestate_class import IonosphereState
from src.bindings.coordinates_class import LLA_Coord
from src.raystate_class import RayState

class AbstractSpacePhysicsModel(ABC):

    def __init__(self, ionosphereState: IonosphereState, currentDateTime: datetime):
        self.ionosphereState = ionosphereState
        self.currentDateTime = currentDateTime
        super().__init__()

    @abstractmethod
    def generatePointEstimate(self, rayPoint : LLA_Coord):
        pass

    @abstractmethod
    def generateSetEstimate(self, rayPoints : list[LLA_Coord]):
        pass
    
    @abstractmethod
    def generateSetEstimateFromRayState(self,  rayStates : list[RayState]):
        pass