import tkinter as tk
from views.mainView import MainView
from controllers.AppController import AppController


def main():
    """Funzione principale per avviare l'applicazione"""
    # Crea il controller principale
    app_controller = AppController()
    
    # Crea la finestra principale
    root = tk.Tk()
    app_controller.set_current_window(root)
    
    # Crea la main view passando il controller
    main_view = MainView(root, app_controller)
    
    root.mainloop()


if __name__ == "__main__":
    main()
