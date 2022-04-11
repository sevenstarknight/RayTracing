import numpy as np

class VectorArray():
    def __init__(self, x:float, y:float, z:float):
        self.data = np.array([x,y,z])