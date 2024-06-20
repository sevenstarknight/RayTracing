# STDLIB modules
from abc import ABC, abstractmethod
from datetime import datetime

# FIRSTPARTY modules
from src.bindings.models.ionospherestate_class import IonosphereState
from src.bindings.positional.layer_class import Layer

class AbstractSpacePhysicsModel(ABC):

    def __init__(self, ionosphereState: IonosphereState, currentDateTime: datetime):
        self.ionosphereState = ionosphereState
        self.currentDateTime = currentDateTime

    @abstractmethod
    def generatePointEstimate(self, layer : Layer):
        pass

    @abstractmethod
    def generateSetEstimate(self, layer : list[Layer]):
        pass