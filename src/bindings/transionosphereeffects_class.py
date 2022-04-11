# ====================================================
# local imports
from raystate_class import RayState

class TransIonosphereEffects():
    def __init__(self, rayState:list[RayState], totalIonoDelay_sec:float, totalIonoLoss_db:float):
        self.rayState = rayState
        self.totalIonoDelay_sec = totalIonoDelay_sec
        self.totalIonoLoss_db = totalIonoLoss_db