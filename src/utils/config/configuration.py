








OUTPUT_COLUMNS = [
    "NOME PA", "CER", "nome DEST", "nome TRASP", 
    "numero_formulario", "data_raccolta", "kg", 
    "Cod.Smalt.", "Produttore rifiuto"
]


ELABORATORE_CONFIG = {

    "GECO": {
        "import_method": "upload_csvGECO",
        "process_method": "elaborate_geco",
        "delimiter": ";"
    },
    "APRICA": {
        "import_method": "upload_csvAPRICA",
        "process_method": "elaborate_aprica"
    },
    "VALCAVALLINA": {
        "import_method": "uploadCSV_VCS",
        "process_method": "elabVCS"
    },
    "ALTRO": {
        "import_method": "upload_csvALTRO",
        "process_method": "elaborate_altro"
    }
}