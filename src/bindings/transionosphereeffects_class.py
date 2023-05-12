# ====================================================
# local imports
from src.bindings.raytracer.rayvector_class import RayVector


class TransIonosphereEffects():
    def __init__(self, rayVectors: list[RayVector], totalIonoDelay_sec: float,
                 totalIonoLoss_db: float, totalGeoDistance_m: float):
        self.rayVectors = rayVectors
        self.totalIonoDelay_sec = totalIonoDelay_sec
        self.totalIonoLoss_db = totalIonoLoss_db
        self.totalGeoDistance_m = totalGeoDistance_m
