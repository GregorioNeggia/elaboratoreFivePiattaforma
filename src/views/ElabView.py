from utils.config.configuration import ELABORATION_CONFIG
from utils.config.configuration import OUTPUT_COLUMNS



class ElaboratoreView:

    def __init__ (self, root, scelta):
        self.root = root
        self.scelta = scelta
        self.columns = OUTPUT_COLUMNS  
        self.config = ELABORATION_CONFIG[scelta]