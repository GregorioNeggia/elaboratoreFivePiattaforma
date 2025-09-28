

import pandas as pd


class AppController:

    def __init__(self, csv_controller, config, elab_controller, columns):
        self.csv_controller = csv_controller
        self.config = config
        self.elab_controller = elab_controller
        self.columns = columns





    def apri_elaboratore(self, scelta):
        from tkinter import Toplevel
        from views.ElabView import ElaboratoreView

        # Crea una nuova finestra per l'elaboratore
        elab_window = Toplevel()
        elab_window.title(f"Elaboratore - {scelta}")
        elab_window.geometry("800x600")

        # Crea la vista dell'elaboratore passando la scelta e il controller
        elab_view = ElaboratoreView(elab_window, scelta, self)
        elab_window.mainloop()

    def apriInfo(self):
        from views.InfoView import InfoView
        InfoView()


    




    def elaborazione(self, nomePa, trasportatore, scelta, pathIn):
        elab_config = self.config["ELABORATORE_CONFIG"].get(scelta)
        if not elab_config:
            raise ValueError(f"Configurazione non trovata per la scelta: {scelta}")

        metodoImportNome = elab_config["import_method"]
        metodoElabNome = elab_config["process_method"]

        metodoImport = getattr(self.csv_controller, metodoImportNome)
        metodoElab = getattr(self.elab_controller, metodoElabNome)

        try:
            df = metodoImport(pathIn)
            dfOut = metodoElab(df, self.columns, nomePa, trasportatore)
            return dfOut

        except AttributeError as e:
            print(f"Errore: Metodo non trovato - {e}")
        except Exception as e:
            print(f"Errore imprevisto durante l'elaborazione: {e}")
        return None




            
