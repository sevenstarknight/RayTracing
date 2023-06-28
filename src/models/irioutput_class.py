from xarray import Dataset
import pandas as pd

class IRIOutput():

    def __init__(self):
        self.n_e: float = 0
        self.T_n: float = 0
        self.T_i: float = 0
        self.T_e: float = 0

        self.nO_Ion: float = 0
        self.nH_Ion: float = 0
        self.nHe_Ion: float = 0
        self.nCI_Ion: float = 0
        self.nN_Ion: float = 0

    @classmethod
    def from_geoprofile(cls, iono1: Dataset, iono2: Dataset):
        df : pd.DataFrame = iono1.to_dataframe()
        classIri = cls()

        #! is there a better way to handle this?
        classIri.n_e  = df[df["ne"] != -1 ]["ne"].mean()

        classIri.T_n = df[df["Tn"] != -1 ]["Tn"].mean()
        classIri.T_i = df[df["Ti"] != -1 ]["Ti"].mean()
        classIri.T_e = df[df["Te"] != -1 ]["Te"].mean()

        classIri.nO_Ion = df[df["nO+"] != -1 ]["nO+"].mean()
        classIri.nH_Ion = df[df["nH+"] != -1 ]["nH+"].mean()
        classIri.nHe_Ion = df[df["nHe+"] != -1 ]["nHe+"].mean()
        classIri.nCI_Ion = df[df["nCI"] != -1 ]["nCI"].mean()
        classIri.nN_Ion = df[df["nN+"] != -1 ]["nN+"].mean()

        return(classIri)
    
    @classmethod
    def from_xarray(cls, iono: Dataset):
        df : pd.DataFrame = iono.to_dataframe()
        classIri = cls()

        #! is there a better way to handle this?
        classIri.n_e  = df[df["ne"] != -1 ]["ne"].mean()

        classIri.T_n = df[df["Tn"] != -1 ]["Tn"].mean()
        classIri.T_i = df[df["Ti"] != -1 ]["Ti"].mean()
        classIri.T_e = df[df["Te"] != -1 ]["Te"].mean()

        classIri.nO_Ion = df[df["nO+"] != -1 ]["nO+"].mean()
        classIri.nH_Ion = df[df["nH+"] != -1 ]["nH+"].mean()
        classIri.nHe_Ion = df[df["nHe+"] != -1 ]["nHe+"].mean()
        classIri.nCI_Ion = df[df["nCI"] != -1 ]["nCI"].mean()
        classIri.nN_Ion = df[df["nN+"] != -1 ]["nN+"].mean()

        return(classIri)

    # 'ne', 'Tn', 'Ti', 'Te', 'nO+', 'nH+', 'nHe+', 'nCI', 'nN+'
    @classmethod
    def from_empty(cls):
        classIri = cls()

        classIri.n_e = -1.0

        classIri.T_n = -1.0
        classIri.T_i = -1.0
        classIri.T_e = -1.0

        classIri.nO_Ion = -1.0
        classIri.nH_Ion = -1.0
        classIri.nHe_Ion = -1.0
        classIri.nCI_Ion = -1.0
        classIri.nN_Ion = -1.0

        return classIri


    def doesExist(self) -> bool:
        if(self.n_e == -1.0):
            return False
        else:
            return True
