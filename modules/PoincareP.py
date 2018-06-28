from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QSplitter, QFileDialog, 
                             QMessageBox, QLabel, QWidget, QCheckBox, QFormLayout, 
                             QLineEdit)
from PyQt5.QtCore import Qt

import pyqtgraph as pg 
from modules.Operations import Operations
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
import seaborn as sns

class PoincareP(QHBoxLayout):
    
    def __init__(self):      
        super().__init__()
        self.initUI()
        
#%%
    def loadSignal(self,bot):
        if (bot==1):
            self.nameS1 = QFileDialog.getOpenFileName(None, 'Open file', '/home')
            if(self.nameS1[0] !=''):
                self.btnLoadS1.setStyleSheet("background-color:#e8f5e9")
                names=str.split(self.nameS1[0],"/")
                t=len(names)
                self.lblS1.setText(names[t-1])
        elif (bot==2):
            self.nameS2=QFileDialog.getOpenFileName(None, 'Open file', '/home')
            if(self.nameS2[0]!=''):
                self.btnLoadS2.setStyleSheet("background-color:#e8f5e9")
                names=str.split(self.nameS2[0],"/")
                t=len(names)
                self.lblS2.setText(names[t-1])

#%%
    def enableFields(self):
        self.lblGrade.setEnabled(True)
        self.txtN.setEnabled(True)
        self.lblFc.setEnabled(True)
        self.txtFc.setEnabled(True)


#%%     
    def showDialog(self):
        if((self.nameS1[0] !='')&(self.nameS2[0]!='')):
            self.scaPoinc.clear()
            self.s1 = pd.read_csv(self.nameS2[0])
            self.s1 = self.s1.as_matrix()
            t1 = self.s1.shape[0]
            self.s1 = self.s1.reshape((t1,))
            self.s2 = pd.read_csv(self.nameS2[0])
            self.s2 = self.s2.as_matrix()
            t2 = self.s2.shape[0]
            self.s2 = self.s2.reshape((t2,))
            lag = int(self.txtLag.text())
            if(self.checkFilter.isChecked()):
                N =int(self.txtN.text())
                fc = int(self.txtFc.text())
                self.s1 = Operations.butter_lowpass_filter(self.s1, fc, 100, N)
                self.s2 = Operations.butter_lowpass_filter(self.s2, fc, 100, N)
            if(lag > 0):
                self.s1, self.s2 = Operations.graphPoinc(self.s1, self.s2, lag)
                if ( len(self.s1)==0):
                    QMessageBox.critical(None, "Alerta","You must select a minor lag", QMessageBox.Ok)
            tam = self.s1.shape[0]
            c1, c2 = Operations.centerPoints(self.s1,self.s2)
            
            spots = [{'pos': [self.s1[i], self.s2[i]], 'data': 1, 'brush':pg.intColor(2,3,alpha=120), 'symbol': 'o', 'size': 10} for i in range(tam)]
            spots.append({'pos': [c1, c2], 'data': 1, 'brush':pg.intColor(3,3,alpha=255), 'symbol': 'o', 'size': 10})
            self.scaPoinc.addPoints(spots)
            self.poinc.addItem(self.scaPoinc)
            sd1 = (np.std(self.s1-self.s2))/(np.sqrt(2))
            sd2 = (np.std(self.s1+self.s2))/(np.sqrt(2))
            self.txtsd1.setText(str(sd1))
            self.txtsd2.setText(str(sd2))
            self.txtc1.setText(str(c1))
            self.txtc2.setText(str(c2))
            
            fig = plt.figure()
            ax = fig.add_subplot(111, aspect='equal')
            ax.plot(self.s1,self.s2, 'b.', alpha=0.5, lw=2)
            ax.plot(c1,c2,'r.')
            el = Ellipse((c1, c2), sd1*2, sd2*2, fill=False, angle=-45, linewidth=1, zorder=2,color='r')
            el.set_clip_box(ax.bbox)
            ax.add_artist(el)
            sns.despine()
            
            plt.tight_layout()
            n1=str.split(self.nameS1[0],"/")
            t=len(n1)
            n11=n1[t-1]
            n111=''
            for i in range(t-1):
                n111=n111+n1[i]+'/'
            n2=str.split(self.nameS2[0],"/")
            t=len(n2)
            n2=n2[t-1]
            nom = n111+n11+"-"+n2+'.png'
            print(nom)
            plt.savefig(nom, transparent=False)
            plt.show()
            
        else:
            QMessageBox.critical(None, "Alerta","You must select tow files", QMessageBox.Ok)

        
#%% 
    def initUI(self):
        pg.setConfigOption('background', 'w')
        
        params = {
                'figure.figsize': [4, 4],
                'figure.dpi': 300,
                'savefig.dpi': 300
           }
        plt.rcParams.update(params)
        
        sns.set()
        sns.set_style("white")
        sns.set_palette("muted")
        sns.set_context("paper")
        
        #Los datos de las señales
        self.s1=[]
        self.s2=[]
        
        self.nameS1=''
        self.nameS2=''
        
        contain=QSplitter(Qt.Horizontal)
        
        buttons = QtWidgets.QVBoxLayout()
        lagBox = QFormLayout()
        filterBox = QFormLayout()
        graphics = QtWidgets.QVBoxLayout()
        viewBox = pg.GraphicsLayoutWidget()
        results =  QFormLayout()
        
        #Componentes de panel botones
        self.btnLoadS1 = QPushButton('Load S1')
        self.btnLoadS1.clicked.connect(lambda: self.loadSignal(1))
        self.btnLoadS1.setStyleSheet("background-color:#fbe9e7")
        self.lblS1 = QLabel('')
        
        self.btnLoadS2 = QPushButton('Load S2')
        self.btnLoadS2.clicked.connect(lambda: self.loadSignal(2))
        self.btnLoadS2.setStyleSheet("background-color:#fbe9e7")       
        self.lblS2 = QLabel('')
        
        self.txtLag = QLineEdit('0')
        self.txtLag.setEnabled(True)
        
        lagBox.addRow("LAG",  self.txtLag)
        
        self.checkFilter = QCheckBox('Filter Apply')
        self.checkFilter.toggled.connect(self.enableFields)
        
        self.lblGrade = QLabel("Filter Grade")
        self.lblGrade.setDisabled(True)        
        self.txtN = QLineEdit('3')
        self.txtN.setDisabled(True)
        
        self.lblFc = QLabel("Cut Frequency")
        self.lblFc.setDisabled(True)        
        self.txtFc = QLineEdit('10')
        self.txtFc.setDisabled(True)
        
        filterBox.addRow(self.lblGrade, self.txtN)
        filterBox.addRow(self.lblFc, self.txtFc)
    
        self.btnDo = QPushButton("Do")
        self.btnDo.setEnabled(True)
        self.btnDo.clicked.connect(self.showDialog)
    
        #Componentes de panel Gráficas
        self.poinc = viewBox.addPlot(row=0, col=1, lockAspect=True)
        self.scaPoinc=pg.ScatterPlotItem()

        self.lblsd1 = QLabel("SD1: ")
        self.lblsd1.setEnabled(True)        
        self.txtsd1 = QLineEdit('')
        self.txtsd1.setEnabled(True)
        
        self.lblsd2 = QLabel("SD2: ")
        self.lblsd2.setEnabled(True)        
        self.txtsd2 = QLineEdit('')
        self.txtsd2.setEnabled(True)
        
        self.lblc1 = QLabel("C11: ")
        self.lblc1.setEnabled(True)        
        self.txtc1 = QLineEdit('')
        self.txtc1.setEnabled(True)
        
        self.lblc2 = QLabel("C2: ")
        self.lblc2.setEnabled(True)        
        self.txtc2 = QLineEdit('')
        self.txtc2.setEnabled(True)
        
        results.addRow(self.lblsd1, self.txtsd1)
        results.addRow(self.lblsd2, self.txtsd2)
        results.addRow(self.lblc1, self.txtc1)
        results.addRow(self.lblc2, self.txtc2)


        graphics.addWidget(viewBox)
        graphics.addLayout(results)
        
        buttons.setSizeConstraint(0)
        buttons.addWidget(self.btnLoadS1)
        buttons.addWidget(self.lblS1)
        buttons.addWidget(self.btnLoadS2)
        buttons.addWidget(self.lblS2)
        buttons.addLayout(lagBox)
        buttons.addWidget(self.checkFilter)
        buttons.addLayout(filterBox)
        buttons.addWidget(self.btnDo)

        bot = QWidget()
        bot.setLayout(buttons)
        gra = QWidget()
        gra.setLayout(graphics)
        
        
        contain.addWidget(bot)
        contain.addWidget(gra)
        self.addWidget(contain)

        
