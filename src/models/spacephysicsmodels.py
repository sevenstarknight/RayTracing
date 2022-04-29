# ====================================================
# local imports
from src.models.igrf_model import IGRF_Model
from src.models.iri_model import IRI_Model
from src.models.msise_model import MSISE_Model


class SpacePhysicsModels():
    def __init__(self, igrf: IGRF_Model, msise: MSISE_Model, iri: IRI_Model):
        self.igrf = igrf
        self.msise = msise
        self.iri = iri
