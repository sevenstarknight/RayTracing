from abc import ABC, abstractmethod
from datetime import datetime

## ====================================================
# local imports
from src.bindings.ionospherestate_class import IonosphereState
from src.rayvector_class import RayVector

class AbstractSpacePhysicsModel(ABC):

    def __init__(self, ionosphereState: IonosphereState, currentDateTime: datetime):
        self.ionosphereState = ionosphereState
        self.currentDateTime = currentDateTime
        super().__init__()

    @abstractmethod
    def generatePointEstimate(self, rayVector : RayVector):
        pass

    @abstractmethod
    def generateSetEstimate(self, rayVector : list[RayVector]):
        pass