from tkinter import ttk, messagebox, simpledialog
import tkinter as tk
import os

class InfoView:

    def __init__(self, parent=None):
        if parent:
            self.window = tk.Toplevel(parent)
        else:
            self.window = tk.Toplevel()
        
        self.window.title("Guida - Elaboratore Five")
        self.window.geometry("1000x800")  # Increased size for better readability
        self.window.configure(bg="#002244")  # Slightly darker background for elegance
        self.window.resizable(True, True)  # Allow resizing for flexibility

        # Frame principale
        main_frame = tk.Frame(self.window, bg="#002244", padx=30, pady=30)
        main_frame.pack(fill="both", expand=True)

        # Titolo
        title_label = tk.Label(main_frame, 
                               text="Guida all'Elaboratore Five", 
                               font=("Helvetica", 24, "bold"),
                               fg="#FFA500",  # Softer orange for better contrast
                               bg="#002244")
        title_label.pack(pady=(0, 30))

        # Testo guida
        guida_text = (
            "Benvenuto nell'Elaboratore Five!\n\n"
            "Questa applicazione ti permette di elaborare file CSV per diverse modalità:\n\n"
            "1. **GECO**: Elabora dati per GECO.\n"
            "2. **APRICA**: Elabora dati per APRICA.\n"
            "3. **VALCAVALLINA**: Elabora dati per VALCAVALLINA (riconoscimento centri raccolta).\n"
            "4. **ALTRO**: Per elaborazioni personalizzate.\n\n"
            "Passi per usare l'app:\n"
            "- Seleziona una modalità cliccando il pulsante corrispondente.\n"
            "- Nella finestra che si apre, importa un file CSV.\n"
            "- Inserisci il nome PA e seleziona il trasportatore.\n"
            "- L'app elaborerà i dati e mostrerà l'anteprima.\n"
            "- Esporta il risultato finale.\n\n"
            "Per assistenza, contatta Gregorio Neggia."
        )

        guida_label = tk.Label(main_frame, 
                               text=guida_text, 
                               font=("Helvetica", 14),  # Larger font for readability
                               fg="white", 
                               bg="#002244",
                               justify="left",
                               wraplength=700)  # Increased wrap length for wider text
        guida_label.pack(pady=(0, 30))

        # Pulsante chiudi
        close_button = tk.Button(main_frame, 
                                text="Chiudi",
                                font=("Arial", 18, "bold"),
                                bg="#FF8C00",
                                fg="#16213E",
                                relief="raised",
                                borderwidth=3,
                                command=self.window.destroy)
        close_button.pack(pady=(0, 20))



