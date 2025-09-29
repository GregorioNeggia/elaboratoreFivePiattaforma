
import csv
from datetime import datetime
from operator import index
import pandas as pd

class ElabController:

    

    def __init__(self):
        pass









    


    """METODI PER VCS"""
    def elabVCS(self, df, columns, nomePa, trasportatore):
        try:
            dfOut = pd.DataFrame(index=range(len(df)), columns=columns)
            for index, row in df.iterrows():
                dfOut.loc[index, "NOME PA"] = "Comune di " + nomePa
                dfOut.loc[index, "CER"] = row.iloc[2]
                dfOut.loc[index, "nome DEST"] = row.iloc[1]
                dfOut.loc[index, "nome TRASP"] = trasportatore["nome"]
                dfOut.loc[index, "numero_formulario"] = row.iloc[6]
                dfOut.loc[index, "data_raccolta"] = row.iloc[5]
                dfOut.loc[index, "kg"] = row.iloc[4]
                dfOut.loc[index, "Cod.Smalt."] = row.iloc[3]

                if row['CDR'] == 1:
                    dfOut.loc[index, "Produttore rifiuto"] = "Comune di " + nomePa + ("(CDR)")
                else:
                    dfOut.loc[index, "Produttore rifiuto"] = "Comune di " + nomePa + ("(M)")
            
            # Sostituisci NaN con stringhe vuote
            dfOut = dfOut.fillna("").infer_objects(copy=False)
            return dfOut

        except Exception as e:
            print(f"Errore imprevisto durante l'elaborazione VCS: {e}")
            return None
        

    """METODI GECO"""

    def elabGECO(self, df, columns, nomePa, trasportatore):
        try:
            dfOut = pd.DataFrame(index=range(len(df)), columns=columns)
            for index, row in df.iterrows():
                dfOut.loc[index, "NOME PA"] = "Comune di " + nomePa
                dfOut.loc[index, "CER"] = row.iloc[2]
                dfOut.loc[index, "nome DEST"] = row.iloc[1]
                dfOut.loc[index, "nome TRASP"] = trasportatore["nome"]
                dfOut.loc[index, "numero_formulario"] = row.iloc[6]
                dfOut.loc[index, "data_raccolta"] = row.iloc[5]
                dfOut.loc[index, "kg"] = row.iloc[4]
                dfOut.loc[index, "Cod.Smalt."] = row.iloc[3]

            if row['CDR'] == 1:
              dfOut.loc[index, "Produttore rifiuto"] = "Comune di " + nomePa + ("(CDR)")
            else:
              dfOut.loc[index, "Produttore rifiuto"] = "Comune di " + nomePa + ("(M)")
            dfOut=dfOut.fillna("").infer_objects(copy=False)
            return dfOut

        except Exception as e:
            print(f"Errore imprevisto durante l'elaborazione G.ECO: {e}")
            return None
        