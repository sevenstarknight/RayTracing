
from dataclasses import dataclass

# THIRDPARTY modules
import numpy as np

@dataclass
class Quantization:
    representationPoints: np.array
    intervalEndPoints: np.array
