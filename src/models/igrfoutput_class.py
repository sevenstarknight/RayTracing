import math
from dataclasses import dataclass


@dataclass
class IGRFOutput:
    Be: float
    Bn: float
    Bu: float

    def getMagnitude(self) -> float:
        return math.sqrt(self.Be * self.Be + self.Bn * self.Bn + self.Bu * self.Bu)
