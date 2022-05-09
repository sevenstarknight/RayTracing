# ====================================================
# local imports
from src.raystate_class import RayState

class TransIonosphereEffects():
    def __init__(self, rayStates:list[RayState], totalIonoDelay_sec:float, 
    totalIonoLoss_db:float, totalGeoDistance_sec:float):
        self.rayStates = rayStates
        self.totalIonoDelay_sec = totalIonoDelay_sec
        self.totalIonoLoss_db = totalIonoLoss_db
        self.totalGeoDistance_sec = totalGeoDistance_sec