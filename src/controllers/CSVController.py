import csv
import io
import pandas as pd
import json
from utils.config.configuration import OUTPUT_COLUMNS

PATH_OUT = "utils/Csv/import(13).csv"
PATH_TRASP = "utils/Db/Trasportatori.json"


class CSVController:

    

    def __init__(self):
        self.PATH_OUT = PATH_OUT
        self.PATH_TRASP = PATH_TRASP
        

    

    def uploadOutput(self):
        try:
            with open(self.PATH_OUT, mode='r', encoding='utf-8') as file:
                df = pd.read_csv(file)
                return df
        except FileNotFoundError:
            print(f"Errore: Il file '{self.PATH_OUT}' non è stato trovato.")
        except pd.errors.EmptyDataError:
            print(f"Errore: Il file '{self.PATH_OUT}' è vuoto o non contiene dati validi.")
        except Exception as e:
            print(f"Errore imprevisto: {e}")

            

    def caricaTrasp(PATH_TRASP, idTrasp):
        try:
            with open(PATH_TRASP, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for item in data:
                    if item['id'] == idTrasp:
                        print(f"Trasportatore con id '{idTrasp}' trovato: {item}")
                        return item
                    else:
                        print(f"Trasportatore con id '{idTrasp}' non trovato.")
                return None
        except FileNotFoundError:
            print(f"Errore: Il file '{PATH_TRASP}' non è stato trovato.")
        except json.JSONDecodeError:
            print(f"Errore: Il file '{PATH_TRASP}' non contiene JSON valido.")
        except Exception as e:
            print(f"Errore imprevisto: {e}")
        return None
    

    
    

    

    """CARICAMENTI CSV"""




    """METODI PER GECO"""
    def upload_csvGECO(self,path):
        colonne_da_leggere = [1,3,5,6,8,9,10]
        try:
            with open(path, mode='r', encoding='utf-8') as file:
                df = pd.read_csv(file, usecols=colonne_da_leggere, sep=';', header=1)
                # Rimuovi righe dove la quarta colonna è vuota o contiene la parola "totale" (case-insensitive)
                col4 = df.iloc[:, 3]
                non_empty = col4.notna() & (col4.astype(str).str.strip() != '')
                not_totale = ~col4.astype(str).str.lower().str.contains('Totale', na=False)
                df = df[non_empty & not_totale].reset_index(drop=True)

                df['CDR'] = df.iloc[:, 0].apply(lambda x: 1 if "CDR" in str(x) else 0)
                return df
            
        except FileNotFoundError:
            print(f"Errore: Il file '{path}' non è stato trovato.")
        except pd.errors.EmptyDataError:
            print(f"Errore: Il file '{path}' è vuoto o non contiene dati validi.")
        except Exception as e:
            print(f"Errore imprevisto: {e}")

    

    """METODI PER APRICA"""
    def upload_csvAPRICA(path):
        pass





    """METODI PER VCS"""
    def uploadCSV_VCS(self, path):
        
        colonne_da_leggere = [1,5,6,8,9,10,12]

        try:
            with open(path, mode='r', encoding='utf-8') as file:
                
                df = pd.read_csv(file, usecols=colonne_da_leggere, sep=';', header=0)

                df['CDR'] = df.iloc[:, 0].apply(lambda x: 1 if "CENTRO RACCOLTA" in str(x) else 0)

                return df
        except FileNotFoundError:
            print(f"Errore: Il file '{path}' non è stato trovato.")
        except pd.errors.EmptyDataError:
            print(f"Errore: Il file '{path}' è vuoto o non contiene dati validi.")
        except Exception as e:
            print(f"Errore imprevisto: {e}")





    """METODI PER ALTRO"""
    def upload_csvALTRO(path):
        pass








        """METODO EXPORT CSV"""
    @staticmethod
    def esporta(table):
        """
        Esporta i dati dalla tabella Treeview in un file CSV
        """
        try:
            # Ottieni tutte le righe dalla tabella
            rows = []

            for row_id in table.get_children():
                row_values = table.item(row_id, 'values')
                rows.append(list(row_values))

            if not rows:
                print("Nessun dato da esportare nella tabella")
                return

            # Crea DataFrame dai dati della tabella
            df = pd.DataFrame(rows, columns=OUTPUT_COLUMNS)

            # Chiedi all'utente dove salvare il file
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("File CSV", "*.csv"), ("Tutti i file", "*.*")],
                title="Salva file CSV esportato"
            )

            if file_path:
                # Usa il metodo esistente per esportare
                df.to_csv(file_path, index=False, header=OUTPUT_COLUMNS, sep=';')
                print(f"Dati esportati con successo in: {file_path}")
            else:
                print("Esportazione annullata dall'utente")

        except Exception as e:
            print(f"Errore durante l'esportazione: {e}")
    


