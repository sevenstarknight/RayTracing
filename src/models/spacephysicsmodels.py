# ====================================================
# local imports
from models.igrf_model import IGRF_Model
from models.iri_model import IRI_Model
from models.msise_model import MSISE_Model


class SpacePhysicsModels():
    def __init__(self, igrf: IGRF_Model, msise: MSISE_Model, iri: IRI_Model):
        self.igrf = igrf
        self.msise = msise
        self.iri = iri
