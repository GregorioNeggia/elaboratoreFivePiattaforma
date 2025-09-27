import tkinter as tk
from tkinter import ttk
import os

class MainView:
    def __init__(self, root, AppController):
        self.root = root
        self.AppController = AppController
        self.root.title("Elaboratore Five - Seleziona Modalità")
        self.root.geometry("700x550")
        self.root.configure(bg="#1956E4")  # Blu scuro sfondo
        
        # Carica il logo
        logo_path = "src/utils/five_consulting_logo.png"
        if os.path.exists(logo_path):
            try:
                self.logo = tk.PhotoImage(file=logo_path)
                print("Logo caricato con successo.")
            except Exception as e:
                print(f"Errore caricamento logo: {e}")
                self.logo = None
        else:
            print(f"File logo non trovato: {logo_path}")
            self.logo = None
        
        # Configurazione del grid principale
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Frame principale con sfondo blu scuro
        self.main_frame = tk.Frame(self.root, bg="#003366", padx=20, pady=20)
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.columnconfigure(0, weight=1)

        self.logo_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        self.logo_frame.grid(row=0, column=0, pady=(0, 10))
        self.info_frame = tk.Frame(self.main_frame, bg="#003366")
        self.info_frame.grid(row=1, column=0)
        
        # Logo
        if self.logo:
            self.logo_label = tk.Label(self.logo_frame, image=self.logo, bg="#FFFFFF")
            self.logo_label.grid(row=0, column=0, pady=(0, 5))
        
        # Banda bianca sotto il logo
        self.band_frame = tk.Frame(self.logo_frame, bg="white", height=3)
        self.band_frame.grid(row=1, column=0, pady=(0, 15), sticky=(tk.W, tk.E))
        
        # Titolo
        self.title_label = tk.Label(self.info_frame, 
                                   text="Elaboratore Five", 
                                   font=("Arial", 24, "bold"),
                                   fg="#FF6600",  # Arancione
                                   bg="#003366")
        self.title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Sottotitolo
        self.subtitle_label = tk.Label(self.info_frame, 
                                      text="Seleziona la modalità di elaborazione", 
                                      font=("Arial", 14),
                                      fg="white",
                                      bg="#003366")
        self.subtitle_label.grid(row=1, column=0, pady=(0, 30))
        
        # Frame per i bottoni
        self.buttons_frame = tk.Frame(self.info_frame, bg="#003366")
        self.buttons_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        self.buttons_frame.columnconfigure(0, weight=1)
        
        # Stile bottoni
        button_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "#FF6600",  # Arancione
            "fg": "white",  # Testo bianco
            "activebackground": "#CC5500",  # Arancione scuro hover
            "activeforeground": "white",
            "relief": "raised",
            "bd": 3,
            "width": 20,
            "height": 2
        }
        
        # Bottoni
        self.button_geco = tk.Button(self.buttons_frame, 
                                    text="GECO", 
                                    command=lambda: self.apri_elaboratore("GECO"),
                                    **button_style)
        self.button_geco.grid(row=0, column=0, padx=10, pady=5, sticky=(tk.W, tk.E))

        self.button_aprica = tk.Button(self.buttons_frame,
                                    text="APRICA", 
                                    command=lambda: self.apri_elaboratore("APRICA"),
                                    **button_style)
        self.button_aprica.grid(row=1, column=0, padx=10, pady=5, sticky=(tk.W, tk.E))

        self.button_vcs = tk.Button(self.buttons_frame,
                                    text="VALCAVALLINA",
                                    command=lambda: self.apri_elaboratore("VALCAVALLINA"),
                                    **button_style)
        self.button_vcs.grid(row=2, column=0, padx=10, pady=5, sticky=(tk.W, tk.E))

        self.button_altro = tk.Button(self.buttons_frame,
                                    text="ALTRO",
                                    command=lambda: self.apri_elaboratore("ALTRO"),
                                    **button_style)
        self.button_altro.grid(row=3, column=0, padx=10, pady=5, sticky=(tk.W, tk.E))

        self.button_info = tk.Button(self.buttons_frame,
                                    text="INFO",
                                    command=lambda: self.AppController.apriInfo(),
                                    **button_style)
        self.button_info.grid(row=4, column=0, padx=10, pady=5, sticky=(tk.W, tk.E))

        # Frame per il footer
        self.footer_frame = tk.Frame(self.info_frame, bg="#003366")
        self.footer_frame.grid(row=3, column=0, pady=(20, 0))
        
        # Label informativa
        self.info_label = tk.Label(self.footer_frame, 
                                  text="DEVELOPED BY GREGORIO NEGGIA", 
                                  font=("Arial", 10),
                                  fg="white",
                                  bg="#003366")
        self.info_label.grid(row=0, column=0)
    
    def apri_elaboratore(self, scelta):
        self.AppController.apri_elaboratore(scelta)