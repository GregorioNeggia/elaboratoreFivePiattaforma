import tkinter as tk
from tkinter import ttk



class MainView:
    def __init__(self, root, AppController):
        self.root = root
        self.AppController = AppController
        self.root.title("Elaboratore Five - Seleziona Modalità")
        self.root.geometry("600x400")
        
        # Configurazione del grid principale
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Frame principale
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.columnconfigure(0, weight=1)
        
        # Titolo
        self.title_label = ttk.Label(self.main_frame, 
                                   text="Elaboratore Five", 
                                   font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Sottotitolo
        self.subtitle_label = ttk.Label(self.main_frame, 
                                      text="Seleziona la modalità di elaborazione", 
                                      font=("Arial", 12))
        self.subtitle_label.grid(row=1, column=0, pady=(0, 30))
        
        # Frame per i bottoni
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        self.buttons_frame.columnconfigure((0, 1), weight=1)
        
        # Bottone GECO
        self.btn_geco = ttk.Button(self.buttons_frame, 
                                 text="GECO", 
                                 command=lambda: self.AppController.apriElabGeco(),
                                 width=15)
        self.btn_geco.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Bottone APRICA
        self.btn_aprica = ttk.Button(self.buttons_frame, 
                                   text="APRICA", 
                                   command=lambda: self.apri_elaboratore("APRICA"),
                                   width=15)
        self.btn_aprica.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Bottone VALCAVALLINA
        self.btn_valcavallina = ttk.Button(self.buttons_frame, 
                                         text="VALCAVALLINA", 
                                         command=lambda: self.apri_elaboratore("VALCAVALLINA"),
                                         width=15)
        self.btn_valcavallina.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Bottone ALTRO
        self.btn_altro = ttk.Button(self.buttons_frame, 
                                  text="ALTRO", 
                                  command=lambda: self.apri_elaboratore("ALTRO"),
                                  width=15)
        self.btn_altro.grid(row=1, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Frame per il footer
        self.footer_frame = ttk.Frame(self.main_frame)
        self.footer_frame.grid(row=3, column=0, pady=(40, 0))
        
        # Label informativa
        self.info_label = ttk.Label(self.footer_frame, 
                                  text="Clicca su una modalità per iniziare l'elaborazione", 
                                  font=("Arial", 10),
                                  foreground="gray")
        self.info_label.grid(row=0, column=0)
    
    def apri_elaboratore(self, scelta):
        """Delega al controller l'apertura della finestra di elaborazione"""
        self.AppController.apri_elaborazione(scelta)