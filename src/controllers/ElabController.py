
import csv
from datetime import datetime
from operator import index
import pandas as pd

class ElabController:


    

    def __init__(self):
        pass



    @staticmethod
    def isDecimal(value):
        try:
            float(value)
            return True
        except ValueError:
            return False




    


    """METODI PER VCS"""
    def elabVCS(self, df, columns, nomePa, trasportatore, percentuale):
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

                try:
                    cdr_val = row.get('CDR', None)
                    if cdr_val is not None and str(cdr_val).strip() != 'nan':
                        if int(float(cdr_val)) == 1:
                            dfOut.loc[index, "Produttore rifiuto"] = "Comune di " + nomePa + ("(CDR)")
                        else:
                            dfOut.loc[index, "Produttore rifiuto"] = "Comune di " + nomePa + ("(M)")
                    else:
                        # valore CDR mancante: default a (M)
                        dfOut.loc[index, "Produttore rifiuto"] = "Comune di " + nomePa + ("(M)")
                except Exception:
                    dfOut.loc[index, "Produttore rifiuto"] = "Comune di " + nomePa + ("(M)")
            
            # Sostituisci NaN con stringhe vuote
            dfOut = dfOut.fillna("").infer_objects(copy=False)
            return dfOut

        except Exception as e:
            print(f"Errore imprevisto durante l'elaborazione VCS: {e}")
            return None
        

    """METODI GECO"""

    def elabGECO(self, df, columns, nomePa, trasportatore, percentuale):

        percentuale = percentuale / 100 if percentuale != 1 else percentuale
        
        try:
            dfOut = pd.DataFrame(index=range(len(df)), columns=columns)
            for index, row in df.iterrows():
                dfOut.loc[index, "NOME PA"] = "Comune di " + nomePa
                dfOut.loc[index, "CER"] = row.iloc[1]
                dfOut.loc[index, "nome DEST"] = row.iloc[4]
                dfOut.loc[index, "nome TRASP"] = trasportatore["nome"]
                dfOut.loc[index, "numero_formulario"] = row.iloc[3]
                dfOut.loc[index, "data_raccolta"] = row.iloc[2]
                dfOut.loc[index, "Cod.Smalt."] = row.iloc[5]
                # Gestione Produttore rifiuto basata su CDR per riga

                
                try:
                    cdr_val = row.get('CDR', None)
                    if cdr_val is not None and str(cdr_val).strip() != 'nan':

                        dfOut.loc[index, "Produttore rifiuto"] = "Comune di " + nomePa + ("(M)")
                        dfOut.loc[index, "kg"] = row.iloc[8]
    
                        if int(float(cdr_val)) == 1:
                            dfOut.loc[index, "Produttore rifiuto"] = "Comune di " + nomePa + ("(CDR)")
                            dfOut.loc[index, "kg"] = float(f"{row.iloc[8] * (percentuale if percentuale is not None else 1):.3f}")
                        
                    else:
                        # valore CDR mancante: default a (M)
                        dfOut.loc[index, "Produttore rifiuto"] = "Comune di " + nomePa + ("(M)")
                except Exception:
                    dfOut.loc[index, "Produttore rifiuto"] = "Comune di " + nomePa + ("(M)")

            # Sostituisci NaN con stringhe vuote (su colonne object) e inferisci i tipi
            try:
                obj_cols = dfOut.select_dtypes(include=["object"]).columns
                if len(obj_cols) > 0:
                    dfOut[obj_cols] = dfOut[obj_cols].fillna("")
                dfOut = dfOut.infer_objects(copy=False)
            except Exception:
                # Fallback semplice
                dfOut = dfOut.fillna("").infer_objects(copy=False)
            return dfOut

        except Exception as e:
            print(f"Errore imprevisto durante l'elaborazione G.ECO: {e}")
            return None
        


        
        