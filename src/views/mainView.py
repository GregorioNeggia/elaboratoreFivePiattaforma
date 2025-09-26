import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Five Consulting - Elaboratore File")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1a1a2e")  # Blu scuro
        self.root.resizable(True, True)
        
        # Centra la finestra sullo schermo
        self.center_window()
        
       
        footerlabel = tk.Label(self.root, text="Developed by Gregorio Neggia", 
                              font=("SF Pro Display", 12), 
                              bg="#1a1a2e", 
                              fg="#ffffff")
        footerlabel.pack(side="bottom", pady=15)
        
        # Container principale con padding elegante
        main_container = tk.Frame(self.root, bg="#1a1a2e")
        main_container.pack(fill="both", expand=True, padx=40, pady=(30, 10))
        
        # Header section
        header_frame = tk.Frame(main_container, bg="#1a1a2e")
        header_frame.pack(fill="x", pady=(0, 40))
        
        # Carica il logo con frame elegante
        try:
            self.logo = PhotoImage(file="src/utils/five_consulting_logo.png")
            # Frame per il logo con bordo sottile
            logo_frame = tk.Frame(header_frame, bg="#2a2a4e", relief="flat", bd=0)
            logo_frame.pack(pady=(0, 20))
            
            logo_label = tk.Label(logo_frame, image=self.logo, bg="#ffffff", 
                                 relief="flat", bd=0)
            logo_label.pack(padx=2, pady=2)
        except Exception as e:
            print(f"Errore nel caricamento del logo: {e}")

        # Titolo principale con tipografia moderna
        title_label = tk.Label(header_frame, 
                              text="Seleziona il tipo di file da elaborare", 
                              font=("SF Pro Display", 18, "normal"), 
                              fg="#ffffff", 
                              bg="#1a1a2e")
        title_label.pack(pady=(0, 10))
        
        # Sottotitolo
        subtitle_label = tk.Label(header_frame, 
                                 text="Scegli il formato corrispondente ai tuoi dati", 
                                 font=("SF Pro Display", 12, "normal"), 
                                 fg="#8b8bb0", 
                                 bg="#1a1a2e")
        subtitle_label.pack()

        # Configurazione stili avanzati
        self.setup_modern_styles()

        # Area bottoni con layout a griglia moderna
        self.create_button_grid(main_container)

        
    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1200x700+{x}+{y}")
    
    def setup_modern_styles(self):
        """Configura stili moderni e eleganti"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Stile bottone principale
        style.configure("Modern.TButton", 
                       font=("SF Pro Display", 14, "normal"),
                       background="#ff6700",
                       foreground="white",
                       relief="flat",
                       borderwidth=0,
                       focuscolor="none")
        
        # Effetti hover
        style.map("Modern.TButton",
                 background=[
                     ("active", "#ff8533"),
                     ("pressed", "#e65c00")
                 ],
                 foreground=[("active", "white"), ("pressed", "white")],
                 relief=[("pressed", "flat")])
    
    def create_button_grid(self, parent):
        """Crea una griglia moderna di bottoni"""
        # Frame per i bottoni con layout centrato
        buttons_container = tk.Frame(parent, bg="#1a1a2e")
        buttons_container.pack(expand=True, fill="both")
        
        # Dati dei bottoni
        button_data = [
            {"name": "GECO", "icon": "🏢"},
            {"name": "APRICA", "icon": "🏔️"},
            {"name": "VALCAVALLINA", "icon": "🏞️"},
            {"name": "ALTRO (in via di sviluppo)", "icon": "📄"}
        ]
        
        # Layout a griglia 2x2
        for i, btn_info in enumerate(button_data):
            row = i // 2
            col = i % 2
            
            # Frame per ogni bottone
            btn_frame = tk.Frame(buttons_container, bg="#2a2a4e", relief="flat", bd=0)
            btn_frame.grid(row=row, column=col, padx=20, pady=15, sticky="nsew", ipadx=10, ipady=10)
            
            # Icona
            icon_label = tk.Label(btn_frame, text=btn_info["icon"], 
                                 font=("Apple Color Emoji", 24), 
                                 bg="#2a2a4e", fg="white")
            icon_label.pack(pady=(15, 5))
            
            # Bottone principale
            button = ttk.Button(btn_frame, 
                               text=btn_info["name"], 
                               style="Modern.TButton",
                               command=lambda t=btn_info["name"]: self.on_button_click(t))
            button.pack(pady=(5, 15), ipadx=25, ipady=10)
            
            # Hover effects
            self.add_hover_effect(btn_frame, button)
        
        # Configura il grid per essere responsive
        for i in range(2):
            buttons_container.columnconfigure(i, weight=1)
            buttons_container.rowconfigure(i, weight=1)
    
    def add_hover_effect(self, frame, button):
        """Aggiunge effetti hover eleganti"""
        original_bg = "#2a2a4e"
        hover_bg = "#3a3a5e"
        
        def on_enter(e):
            frame.configure(bg=hover_bg)
            for child in frame.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(bg=hover_bg)
        
        def on_leave(e):
            frame.configure(bg=original_bg)
            for child in frame.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(bg=original_bg)
        
        # Bind degli eventi a tutti gli elementi del frame
        widgets = [frame] + list(frame.winfo_children())
        for widget in widgets:
            if not isinstance(widget, ttk.Button):  # Non applicare a ttk.Button che ha i suoi stili
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)

    def on_button_click(self, button_text):
        print(f"Hai cliccato: {button_text}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainView(root)
    root.mainloop()