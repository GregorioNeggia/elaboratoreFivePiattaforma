import tkinter as tk
from views.mainView import MainView
from controllers.AppController import AppController
from controllers.CSVController import CSVController
from controllers.ElabController import ElabController
from utils.ui.theme_colors import ThemeColors
from utils.config.configuration import ELABORATORE_CONFIG
from utils.config.configuration import OUTPUT_COLUMNS

def main():
    """Funzione principale per avviare l'applicazione"""
    # Crea il controller principale
    
    app_controller = AppController(CSVController(), {"ELABORATORE_CONFIG": ELABORATORE_CONFIG}, ElabController(), OUTPUT_COLUMNS)
    
    # Crea la finestra principale
    root = tk.Tk()
    
    
    # Crea la main view passando il controller
    main_view = MainView(root, app_controller)
    
    root.mainloop()


if __name__ == "__main__":
    main()
