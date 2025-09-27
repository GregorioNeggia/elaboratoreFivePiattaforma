import tkinter as tk
from views.ElaboratoreView import ElaboratoreView

def main():
    """Funzione principale per avviare l'applicazione"""
    root = tk.Tk()
    app = ElaboratoreView(root)
    root.mainloop()

if __name__ == "__main__":
    main()
