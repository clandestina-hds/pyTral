from PyQt5.QtWidgets import (QMainWindow,QWidget,QPushButton, QSplitter, QHBoxLayout,
                             QGridLayout,QVBoxLayout, QFileDialog, QLabel)
from PyQt5.QtCore import Qt
import pyqtgraph as pg # library needed to plot graphics
import numpy as np
import pandas as pd

#%%
class cutSignals(QHBoxLayout):
    def __init__(self):
        super(cutSignals,self).__init__()
        self.initUI()

        
#%%
    def cargarSenial(self):
        self.plot1.clear()
        self.nombreSenial= QFileDialog.getOpenFileName(None, 'Open file', '/home')
        data = pd.read_csv(self.nombreSenial[0],sep='\t', header=None)
        self.y = data.values
        tam =len(self.y)
        self.y=self.y.reshape((tam,))
        self.x = np.asarray(range(tam))
        self.x=self.x.reshape((tam,))
        self.plot1.plot(self.x, self.y,pen='k')


#%%
    def enabledButtons(self):
        self.btnAdd.setEnabled(True)
        self.btnSegments.setEnabled(True)
        self.plot1.addItem(self.lr)
        
#%%      
    def addInterval(self):
        self.contador = self.contador + 1
        self.valorContador.setText(str(self.contador))
        regionSelected = self.lr.getRegion()
        ini = int(regionSelected[0])
        fin = int(regionSelected[1])
        self.segmentos.append(( ini, fin, fin-ini ))
        
#%%
    def saveData(self):
        self.segmentos = np.asarray(self.segmentos)
        tam = len(self.y)
        t2 = len(self.segmentos)
        if(self.segmentos[0][0] == 0):
            for i in range(t2-1):
                ini = self.segmentos[i][1]
                fin = self.segmentos[i+1][0]
                self.intervalos.append((ini, fin, fin - ini))
            ini = self.segmentos[t2-1][1]
            fin = tam
            self.intervalos.append((ini, fin, fin- ini))
        else:
            ini = 0
            for i in self.segmentos:
                fin = i[0]
                self.intervalos.append((ini, fin, fin - ini))
                ini = i[1]
            self.intervalos.append((ini, tam, tam - ini))
            
        nuevaSenial=self.y[self.segmentos[0,0]:self.segmentos[0,1]]
        df=pd.DataFrame(nuevaSenial)
        df.to_csv(self.nombreSenial[0]+'-Cortada.csv',index=False,mode='w')
        df = pd.DataFrame(self.segmentos)
        df.to_csv(self.nombreSenial[0]+'-CortadaIntervalos.csv',index=False, header = ['Inicio','Fin','Size'], mode = 'w')

#%% 
    def initUI(self):
        pg.setConfigOption('background', 'w')
        
        contain=QSplitter(Qt.Horizontal)
        
        #################################################################
        ##     Definición de variables globales
        #################################################################

        self.nombreSenial=''
        self.x=[]
        self.y=[]
        self.intervalos = []
        self.segmentos = []
        self.contador=0

        
        #################################################################
        ##     Definición de elementos contenedores
        #################################################################
        graficos = QVBoxLayout()
        botones = QVBoxLayout()
        
        
        #################################################################
        ##     Elementos del layout botones
        #################################################################
        
        #Region for segment in signal
        self.lr = pg.LinearRegionItem([300,500])
        
        btnLoadSig = QPushButton('Cargar Senial')
        btnLoadSig.clicked.connect(self.cargarSenial)
        
        self.valorContador = QLabel('')
        
        btnIniciar = QPushButton('Start')
        btnIniciar.clicked.connect(self.enabledButtons)
        
        self.btnAdd=QPushButton('Add Segment')
        self.btnAdd.clicked.connect(self.addInterval)
        self.btnAdd.setEnabled(False)
        
        self.btnSegments=QPushButton('End Segmentation')
        self.btnSegments.clicked.connect(self.saveData)
        self.btnSegments.setEnabled(False)


        #################################################################
        ##     Elementos del layout graficos
        #################################################################
        self.plot1=pg.PlotWidget()
        
        
        #################################################################
        ##     Colocar elementos en layout botones
        #################################################################
        
        botones.addWidget(btnLoadSig)
        botones.addWidget(self.valorContador)
        botones.addWidget(btnIniciar)
        botones.addWidget(self.btnAdd)
        botones.addWidget(self.btnSegments)
        
        #################################################################
        ##     Colocar elementos en layout graficos
        #################################################################
        graficos.addWidget(self.plot1)
        
        #################################################################
        ##     Colocar elementos en la ventana
        #################################################################
        
        bot = QWidget()
        bot.setLayout(botones)
        gra = QWidget()
        gra.setLayout(graficos)

        contain.addWidget(bot)
        contain.addWidget(gra)
        self.addWidget(contain)