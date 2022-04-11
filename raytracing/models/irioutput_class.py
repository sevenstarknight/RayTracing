import xarray


class IRIOutput():
    def __init__(self, iono: xarray.Dataset):
        df = iono.to_dataframe()
        self.iono = df
        self.n_e = df["ne"].iloc[0].item()

        self.T_n = df["Tn"].iloc[0].item()
        self.T_i = df["Ti"].iloc[0].item()
        self.T_e = df["Te"].iloc[0].item()

        self.nO_Ion = df["nO+"].iloc[0].item()
        self.nH_Ion = df["nH+"].iloc[0].item()
        self.nHe_Ion = df["nHe+"].iloc[0].item()
        self.nCI_Ion = df["nCI"].iloc[0].item()
        self.nN_Ion = df["nN+"].iloc[0].item()

        # 'ne', 'Tn', 'Ti', 'Te', 'nO+', 'nH+', 'nHe+', 'nCI', 'nN+'
