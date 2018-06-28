#imports native
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout

# Custom Dependencies
from modules.FractalP import FractalP
from modules.PoincareP import PoincareP
from modules.cutSignals import cutSignals

class mainView(QWidget):
 
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
 
        # Initialize tab screen
        self.tabs = QTabWidget()
        
        self.tabFrac = QWidget()
        self.tabPoinc = QWidget()
        self.tabCut = QWidget()

        
        # Content Tabs
        self.tabFracLayout = FractalP()
        self.tabPoincLayout = PoincareP()
        self.tabCutLayout = cutSignals()


        # Add tabs
        self.tabs.addTab(self.tabFrac,"Fractal")
        self.tabs.addTab(self.tabPoinc,"Poincare")
        self.tabs.addTab(self.tabCut,"Cut Signal")

 
        # Set asing layout
        self.tabFrac.layout = self.tabFracLayout
        self.tabPoinc.layout = self.tabPoincLayout
        self.tabCut.layout = self.tabCutLayout

        
        # SetLayout Tabs
        self.tabFrac.setLayout(self.tabFrac.layout)
        self.tabPoinc.setLayout(self.tabPoinc.layout)
        self.tabCut.setLayout(self.tabCut.layout)
 
        # Add tabs to Main
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)