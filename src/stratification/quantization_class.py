import numpy as np

from dataclasses import dataclass

@dataclass
class Quantization():
    representationPoints: np.array
    intervalEndPoints: np.array