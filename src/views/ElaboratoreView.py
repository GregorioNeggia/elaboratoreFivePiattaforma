import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import PhotoImage
import pandas as pd
import os
import json

class ElaboratoreView:
    def __init__(self, root, file_type="GECO"):
        self.root = root
        self.file_type = file_type
        self.imported_data = None
        self.processed_data = None
        
        self.root.title(f"Five Consulting - Elaboratore {file_type}")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1a1a2e")  # Blu scuro
        self.root.resizable(True, True)
        
        # Centra la finestra sullo schermo
        self.center_window()
        
        # Footer
        footerlabel = tk.Label(self.root, text="Developed by Gregorio Neggia", 
                              font=("SF Pro Display", 12), 
                              bg="#1a1a2e", 
                              fg="#ffffff")
        footerlabel.pack(side="bottom", pady=15)
        
        # Container principale con padding elegante
        main_container = tk.Frame(self.root, bg="#1a1a2e")
        main_container.pack(fill="both", expand=True, padx=40, pady=(30, 10))
        
        # Header section
        self.create_header(main_container)
        
        # Configurazione stili avanzati
        self.setup_modern_styles()
        
        # Area principale divisa in tre sezioni
        self.create_main_sections(main_container)
        
    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")
    
    def create_header(self, parent):
        """Crea la sezione header con logo e titoli"""
        header_frame = tk.Frame(parent, bg="#1a1a2e")
        header_frame.pack(fill="x", pady=(0, 30))
        
        # Carica il logo con frame elegante
        try:
            self.logo = PhotoImage(file="src/utils/five_consulting_logo.png")
            # Frame per il logo con bordo sottile
            logo_frame = tk.Frame(header_frame, bg="#2a2a4e", relief="flat", bd=0)
            logo_frame.pack(pady=(0, 15))
            
            logo_label = tk.Label(logo_frame, image=self.logo, bg="#ffffff", 
                                 relief="flat", bd=0)
            logo_label.pack(padx=2, pady=2)
        except Exception as e:
            print(f"Errore nel caricamento del logo: {e}")

        # Titolo principale con tipografia moderna
        title_label = tk.Label(header_frame, 
                              text=f"Elaboratore File {self.file_type}", 
                              font=("SF Pro Display", 18, "normal"), 
                              fg="#ffffff", 
                              bg="#1a1a2e")
        title_label.pack(pady=(0, 8))
        
        # Sottotitolo
        subtitle_label = tk.Label(header_frame, 
                                 text="Importa, visualizza in anteprima ed esporta i tuoi dati", 
                                 font=("SF Pro Display", 12, "normal"), 
                                 fg="#8b8bb0", 
                                 bg="#1a1a2e")
        subtitle_label.pack()

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
        
        # Stile bottone secondario
        style.configure("Secondary.TButton", 
                       font=("SF Pro Display", 12, "normal"),
                       background="#2a2a4e",
                       foreground="white",
                       relief="flat",
                       borderwidth=0,
                       focuscolor="none")
        
        # Stile bottone di successo
        style.configure("Success.TButton", 
                       font=("SF Pro Display", 14, "normal"),
                       background="#28a745",
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
        
        style.map("Secondary.TButton",
                 background=[
                     ("active", "#3a3a5e"),
                     ("pressed", "#1a1a3e")
                 ],
                 foreground=[("active", "white"), ("pressed", "white")],
                 relief=[("pressed", "flat")])
        
        style.map("Success.TButton",
                 background=[
                     ("active", "#34ce57"),
                     ("pressed", "#218838")
                 ],
                 foreground=[("active", "white"), ("pressed", "white")],
                 relief=[("pressed", "flat")])
        
        # Stile per Treeview
        style.configure("Modern.Treeview", 
                       background="#2a2a4e",
                       foreground="white",
                       fieldbackground="#2a2a4e",
                       font=("SF Pro Display", 10))
        
        style.configure("Modern.Treeview.Heading", 
                       background="#3a3a5e",
                       foreground="white",
                       font=("SF Pro Display", 11, "bold"))
    
    def create_main_sections(self, parent):
        """Crea le sezioni principali riorganizzate"""
        # Frame contenitore per le sezioni
        sections_frame = tk.Frame(parent, bg="#1a1a2e")
        sections_frame.pack(fill="both", expand=True)
        
        # Sezione superiore: Controlli (Importazione e Export)
        controls_frame = tk.Frame(sections_frame, bg="#1a1a2e")
        controls_frame.pack(fill="x", pady=(0, 20))
        
        # Sezione 1: Importazione (sinistra)
        self.create_import_section(controls_frame)
        
        # Sezione 3: Export (destra) 
        self.create_export_section(controls_frame)
        
        # Sezione 2: Anteprima dati (sotto, espansa)
        self.create_preview_section(sections_frame)
        
        # Sezione log in basso
        self.create_activity_log(sections_frame)
    
    def create_import_section(self, parent):
        """Crea la sezione di importazione"""
        # Frame per importazione
        import_frame = tk.Frame(parent, bg="#2a2a4e", relief="flat", bd=0)
        import_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Titolo sezione
        title_label = tk.Label(import_frame, 
                              text="📥 Importazione Dati", 
                              font=("SF Pro Display", 14, "bold"), 
                              fg="#ffffff", 
                              bg="#2a2a4e")
        title_label.pack(pady=(20, 15))
        
        # Info file selezionato
        self.file_info_label = tk.Label(import_frame, 
                                       text="Nessun file selezionato", 
                                       font=("SF Pro Display", 10), 
                                       fg="#8b8bb0", 
                                       bg="#2a2a4e",
                                       wraplength=300)
        self.file_info_label.pack(pady=(0, 15))
        
        # Bottone importa
        import_btn = ttk.Button(import_frame, 
                               text="Seleziona File CSV", 
                               style="Modern.TButton",
                               command=self.import_file)
        import_btn.pack(pady=10, ipadx=20, ipady=8)
        
        # Info statistiche
        self.stats_label = tk.Label(import_frame, 
                                   text="", 
                                   font=("SF Pro Display", 9), 
                                   fg="#8b8bb0", 
                                   bg="#2a2a4e")
        self.stats_label.pack(pady=(10, 0))
    
    def create_preview_section(self, parent):
        """Crea la sezione di anteprima dati con treeview"""
        # Frame per anteprima (espanso verticalmente)
        preview_frame = tk.Frame(parent, bg="#2a2a4e", relief="flat", bd=0)
        preview_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Titolo sezione
        title_label = tk.Label(preview_frame, 
                              text="👁️ Anteprima Dati", 
                              font=("SF Pro Display", 14, "bold"), 
                              fg="#ffffff", 
                              bg="#2a2a4e")
        title_label.pack(pady=(20, 15))
        
        # Frame per treeview con scrollbar
        tree_container = tk.Frame(preview_frame, bg="#2a2a4e")
        tree_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Definisci le colonne standard del CSV
        self.csv_columns = [
            "NOME PA", "CER", "nome DEST", "nome TRASP", 
            "numero_formulario", "data_raccolta", "kg", 
            "Cod.Smalt.", "Produttore rifiuto"
        ]
        
        # Treeview con colonne predefinite
        self.tree = ttk.Treeview(tree_container, style="Modern.Treeview", 
                                show="tree headings", columns=self.csv_columns)
        
        # Configura intestazioni e larghezze colonne
        self.tree.heading("#0", text="ID", anchor="w")
        self.tree.column("#0", width=50, minwidth=40)
        
        column_widths = {
            "NOME PA": 100,
            "CER": 80,
            "nome DEST": 120,
            "nome TRASP": 120,
            "numero_formulario": 130,
            "data_raccolta": 100,
            "kg": 70,
            "Cod.Smalt.": 90,
            "Produttore rifiuto": 130
        }
        
        for col in self.csv_columns:
            self.tree.heading(col, text=col, anchor="w")
            width = column_widths.get(col, 100)
            self.tree.column(col, width=width, minwidth=70)
        
        # Scrollbar verticale
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        # Scrollbar orizzontale
        h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Grid layout per treeview e scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_container.columnconfigure(0, weight=1)
        tree_container.rowconfigure(0, weight=1)
        
        # Aggiungi alcune righe di esempio vuote per mostrare la struttura
        for i in range(5):
            empty_values = ["" for _ in self.csv_columns]
            self.tree.insert("", "end", text=str(i+1), values=empty_values)
        
        # Messaggio iniziale
        self.preview_message = tk.Label(preview_frame, 
                                       text="Struttura tabella predefinita - Importa un file per visualizzare i dati", 
                                       font=("SF Pro Display", 11), 
                                       fg="#8b8bb0", 
                                       bg="#2a2a4e")
        self.preview_message.pack(pady=(10, 0))
    
    def create_export_section(self, parent):
        """Crea la sezione di export"""
        # Frame per export
        export_frame = tk.Frame(parent, bg="#2a2a4e", relief="flat", bd=0)
        export_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Titolo sezione
        title_label = tk.Label(export_frame, 
                              text="📤 Esportazione", 
                              font=("SF Pro Display", 14, "bold"), 
                              fg="#ffffff", 
                              bg="#2a2a4e")
        title_label.pack(pady=(20, 15))
        
        # Info elaborazione
        self.export_info_label = tk.Label(export_frame, 
                                         text="Dati non ancora elaborati", 
                                         font=("SF Pro Display", 10), 
                                         fg="#8b8bb0", 
                                         bg="#2a2a4e",
                                         wraplength=300)
        self.export_info_label.pack(pady=(0, 15))
        
        # Bottone elabora
        self.process_btn = ttk.Button(export_frame, 
                                     text="Elabora Dati", 
                                     style="Secondary.TButton",
                                     command=self.process_data,
                                     state="disabled")
        self.process_btn.pack(pady=5, ipadx=20, ipady=8)
        
        # Bottone export
        self.export_btn = ttk.Button(export_frame, 
                                    text="Esporta CSV", 
                                    style="Success.TButton",
                                    command=self.export_data,
                                    state="disabled")
        self.export_btn.pack(pady=5, ipadx=20, ipady=8)
        
    
    def create_activity_log(self, parent):
        """Crea la sezione log delle attività"""
        # Frame per log attività con altezza fissa
        log_frame = tk.Frame(parent, bg="#2a2a4e", relief="flat", bd=0, height=200)
        log_frame.pack(fill="x", expand=False)
        log_frame.pack_propagate(False)  # Mantieni altezza fissa
        
        # Titolo sezione
        title_label = tk.Label(log_frame, 
                              text="📋 Log Attività", 
                              font=("SF Pro Display", 14, "bold"), 
                              fg="#ffffff", 
                              bg="#2a2a4e")
        title_label.pack(pady=(15, 10))
        
        # Text widget per log con scrollbar
        log_container = tk.Frame(log_frame, bg="#2a2a4e")
        log_container.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        self.log_text = tk.Text(log_container, 
                               bg="#1a1a2e", 
                               fg="#ffffff", 
                               font=("SF Pro Display", 10),
                               wrap="word",
                               state="disabled")
        
        log_scrollbar = ttk.Scrollbar(log_container, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar.pack(side="right", fill="y")
        
        # Messaggio iniziale nel log
        self.add_log_message("🚀 Elaboratore avviato. Pronto per l'importazione dei dati.")
    
    def add_log_message(self, message):
        """Aggiunge un messaggio al log"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state="normal")
        self.log_text.insert("end", formatted_message)
        self.log_text.see("end")
        self.log_text.config(state="disabled")
    
    def import_file(self):
        """Gestisce l'importazione del file CSV"""
        file_path = filedialog.askopenfilename(
            title="Seleziona file CSV",
            filetypes=[("File CSV", "*.csv"), ("Tutti i file", "*.*")]
        )
        
        if file_path:
            try:
                # Carica il file CSV
                self.imported_data = pd.read_csv(file_path)
                
                # Aggiorna le info del file
                filename = os.path.basename(file_path)
                self.file_info_label.config(text=f"File: {filename}")
                
                # Aggiorna le statistiche
                rows, cols = self.imported_data.shape
                self.stats_label.config(text=f"Righe: {rows} | Colonne: {cols}")
                
                # Aggiorna anteprima
                self.update_preview()
                
                # Abilita bottone elaborazione
                self.process_btn.config(state="normal")
                
                # Log
                self.add_log_message(f"✅ File importato: {filename} ({rows} righe, {cols} colonne)")
                
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nell'importazione del file:\n{str(e)}")
                self.add_log_message(f"❌ Errore importazione: {str(e)}")
    
    def update_preview(self):
        """Aggiorna l'anteprima dei dati nel treeview"""
        if self.imported_data is None:
            return
        
        # Aggiorna messaggio
        self.preview_message.config(text="Dati importati - Visualizzazione in corso...")
        
        # Pulisci treeview esistente
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Usa le colonne del CSV importato o quelle predefinite
        imported_columns = list(self.imported_data.columns)
        
        # Verifica se le colonne del CSV corrispondono a quelle predefinite
        columns_match = len(imported_columns) == len(self.csv_columns)
        if columns_match:
            # Usa le colonne predefinite (già configurate)
            display_columns = self.csv_columns
        else:
            # Riconfigura treeview con le nuove colonne
            self.tree.configure(columns=imported_columns)
            display_columns = imported_columns
            
            # Riconfigura intestazioni
            for col in imported_columns:
                self.tree.heading(col, text=col, anchor="w")
                self.tree.column(col, width=120, minwidth=80)
        
        # Aggiungi dati (solo prime 100 righe per performance)
        for idx, row in self.imported_data.head(100).iterrows():
            # Mappa i valori alle colonne corrette
            if columns_match:
                # Se le colonne corrispondono, usa l'ordine predefinito
                values = []
                for col in self.csv_columns:
                    if col in imported_columns:
                        val = row[col]
                        values.append(str(val) if pd.notna(val) else "")
                    else:
                        values.append("")
            else:
                # Usa l'ordine delle colonne importate
                values = [str(val) if pd.notna(val) else "" for val in row.values]
            
            self.tree.insert("", "end", text=str(idx+1), values=values)
        
        # Aggiorna messaggio finale
        total_rows = len(self.imported_data)
        displayed_rows = min(100, total_rows)
        
        if total_rows > 100:
            self.preview_message.config(text=f"Visualizzate {displayed_rows} di {total_rows} righe")
            self.add_log_message(f"ℹ️ Visualizzate prime {displayed_rows} righe di {total_rows}")
        else:
            self.preview_message.config(text=f"Visualizzate tutte le {total_rows} righe")
    
    def process_data(self):
        """Elabora i dati importati"""
        if self.imported_data is None:
            return
        
        try:
            # Simula elaborazione dei dati
            self.add_log_message("🔄 Inizio elaborazione dati...")
            
            # Copia dei dati per elaborazione
            self.processed_data = self.imported_data.copy()
            
            # Qui andrebbe inserita la logica di elaborazione specifica per ogni tipo di file
            # Per ora facciamo una elaborazione di esempio
            
            # Rimuovi righe vuote
            original_rows = len(self.processed_data)
            self.processed_data = self.processed_data.dropna(how='all')
            cleaned_rows = len(self.processed_data)
            
            if original_rows != cleaned_rows:
                self.add_log_message(f"🧹 Rimosse {original_rows - cleaned_rows} righe vuote")
            
            # Aggiorna info export
            self.export_info_label.config(text=f"Dati elaborati: {cleaned_rows} righe pronte")
            
            # Abilita export
            self.export_btn.config(state="normal")
            
            self.add_log_message("✅ Elaborazione completata con successo")
            
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nell'elaborazione:\n{str(e)}")
            self.add_log_message(f"❌ Errore elaborazione: {str(e)}")
    
    def export_data(self):
        """Esporta i dati elaborati"""
        if self.processed_data is None:
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Salva file elaborato",
            defaultextension=".csv",
            filetypes=[("File CSV", "*.csv"), ("Tutti i file", "*.*")]
        )
        
        if file_path:
            try:
                self.processed_data.to_csv(file_path, index=False)
                filename = os.path.basename(file_path)
                self.add_log_message(f"💾 File esportato: {filename}")
                messagebox.showinfo("Successo", f"File esportato correttamente:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nell'esportazione:\n{str(e)}")
                self.add_log_message(f"❌ Errore esportazione: {str(e)}")

def main():
    """Funzione main per test"""
    root = tk.Tk()
    app = ElaboratoreView(root, "GECO")
    root.mainloop()

if __name__ == "__main__":
    main()
