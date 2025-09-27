import pandas as pd
import json




class AppController:
    
    def __init__(self, app_service):
        self.app_service = app_service



    def popolaTabella(self, df):
        """Popola la tabella con i dati del DataFrame"""
        # Pulisce la tabella esistente
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Aggiunge i nuovi dati
        for index, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    