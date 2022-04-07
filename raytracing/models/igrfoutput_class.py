import xarray

class IGRFOutput():
    def __init__(self, igrf:xarray.Dataset):
        self.igrf = igrf.to_dataframe()
    
        