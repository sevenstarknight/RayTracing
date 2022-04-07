import xarray

class IRIOutput():
    def __init__(self, iono:xarray.Dataset):
        self.iono = iono.to_dataframe()
        
        