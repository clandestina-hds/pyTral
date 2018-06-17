# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 21:36:43 2017

@author: Clandestina
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 09:52:17 2016

@author: Clandestina
"""

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QPushButton, QSplitter, QFileDialog, QMessageBox, QLabel, QComboBox,QWidget, QCheckBox, 
                             QLineEdit, QFormLayout)
from PyQt5.QtCore import Qt
import pyqtgraph as pg 
from Operations import Operations
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import seaborn as sns

#%%
class fractalSignal(QWidget):
    def __init__(self):
        super(fractalSignal,self).__init__()
        self.initUI()

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
        
        self.fullSignal=[]
        self.shiftFullSignal=[]
        self.shiftFullSignalNormal=[]
        
        self.fSig=''
        
        contenedor=QtWidgets.QHBoxLayout(self)
        
        contain=QSplitter(Qt.Horizontal)

        buttons = QtWidgets.QVBoxLayout()
        graphics = QtWidgets.QVBoxLayout()
        imaFrac = QtWidgets.QHBoxLayout()
        lagBox = QFormLayout()
        results =  QFormLayout()
       
        self.btnLoadSig = QPushButton('Load Signal')
        self.btnLoadSig.clicked.connect(self.loadSignal)
        self.btnLoadSig.setStyleSheet("background-color:#fbe9e7; font-size: 18px")
        
        self.lblSignal = QLabel('')
        self.lblSignal.setStyleSheet("font-size: 18px")
        
        self.checkTotalSignal = QCheckBox('Signal', self)
        self.checkTotalSignal.setStyleSheet("font-size: 18px")
        

        self.cmbFractal = QComboBox()
        self.cmbFractal.setStyleSheet("background-color:#fbe9e7; font-size: 18px")
        self.cmbFractal.addItem("Triangle") #Elemento 0
        self.cmbFractal.addItem("Square") #Elemento 1
        self.cmbFractal.addItem("Pentagon") #Elemento 2
        self.cmbFractal.addItem("Hexagon") #Elemento 3
        #self.cmbFractal.addItem("Octgon") #Ahora éste es el elemento 4
        
        self.btnDo = QPushButton("Do Fractal")
        self.btnDo.setDisabled(True)
        self.btnDo.setStyleSheet("font-size: 18px")
        self.btnDo.clicked.connect(self.showDialog)

        self.btnFracInter = QPushButton("Points-Inter")
        self.btnFracInter.setDisabled(True)
        self.btnFracInter.setStyleSheet("font-size: 18px")
        self.btnFracInter.clicked.connect(self.update)
        
        self.txtLag = QLineEdit('0')
        self.txtLag.setStyleSheet("font-size: 18px")
        self.txtLag.setEnabled(True)
        lblLag = QLabel("LAG")
        lblLag.setStyleSheet("font-size: 18px")
        
        lagBox.addRow(lblLag,  self.txtLag)
        
        self.btnSub = QPushButton("Graph Poincare")
        self.btnSub.setDisabled(True)
        self.btnSub.setStyleSheet("font-size: 18px")
        self.btnSub.clicked.connect(self.poincSub)
        
        self.lblsd1 = QLabel("SD1: ")
        self.lblsd1.setEnabled(True)  
        self.lblsd1.setStyleSheet("font-size: 18px")
        self.txtsd1 = QLineEdit('')
        self.txtsd1.setEnabled(True)
        self.txtsd1.setStyleSheet("font-size: 18px")
        
        self.lblsd2 = QLabel("SD2: ")
        self.lblsd2.setEnabled(True) 
        self.lblsd2.setStyleSheet("font-size: 18px")
        self.txtsd2 = QLineEdit('')
        self.txtsd2.setEnabled(True)
        self.txtsd2.setStyleSheet("font-size: 18px")
        
        self.lblc1 = QLabel("C11: ")
        self.lblc1.setEnabled(True)  
        self.lblc1.setStyleSheet("font-size: 18px")
        self.txtc1 = QLineEdit('')
        self.txtc1.setEnabled(True)
        self.txtc1.setStyleSheet("font-size: 18px")
        
        self.lblc2 = QLabel("C2: ")
        self.lblc2.setEnabled(True) 
        self.lblc2.setStyleSheet("font-size: 18px")
        self.txtc2 = QLineEdit('')
        self.txtc2.setEnabled(True)
        self.txtc2.setStyleSheet("font-size: 18px")
        
        results.addRow(self.lblsd1, self.txtsd1)
        results.addRow(self.lblsd2, self.txtsd2)
        results.addRow(self.lblc1, self.txtc1)
        results.addRow(self.lblc2, self.txtc2)
        
        self.btnSave = QPushButton("Save Current Data")
        self.btnSave.setDisabled(True)
        self.btnSave.setStyleSheet("font-size: 18px")
        self.btnSave.clicked.connect(self.saveFile)
        
        self.viewBox=pg.GraphicsLayoutWidget()
        self.interFrac = self.viewBox.addPlot()#ViewBox(row=0, col=0, lockAspect=True)
        self.interFrac.setYRange(-0.1, 1.1, padding=0)
        self.interFrac.setXRange(-0.1, 1.1, padding=0)

        self.poinc = self.viewBox.addPlot()#ViewBox(row=0, col=1, lockAspect=True)
        
        self.scaInter=pg.ScatterPlotItem()
        self.scaPoinc=pg.ScatterPlotItem()

        self.roiInter=pg.PolyLineROI([[0.2, 0.5], [0.8, 0.5], [0.5, 0]], pen=(6,9), closed=True)

        imaFrac.addWidget(self.viewBox)

        buttons.setSizeConstraint(0)
        
        buttons.addWidget(self.btnLoadSig)
        buttons.addWidget(self.lblSignal)
        
        buttons.addWidget(self.checkTotalSignal)
        
        nomFractal = QLabel("Fractal Type")
        nomFractal.setStyleSheet("font-size: 18px")
        buttons.addWidget(nomFractal)
        buttons.addWidget(self.cmbFractal)
        
        buttons.addWidget(self.btnDo)
        buttons.addWidget(self.btnFracInter)
        buttons.addLayout(lagBox)
        buttons.addWidget(self.btnSub)
        buttons.addLayout(results)
        buttons.addWidget(self.btnSave)
        
        self.plot1=pg.PlotWidget()
        graphics.addLayout(imaFrac)
        graphics.addWidget(self.plot1)
        bot = QWidget()
        bot.setLayout(buttons)
        gra = QWidget()
        gra.setLayout(graphics)
        
        
        contain.addWidget(bot)
        contain.addWidget(gra)
        contenedor.addWidget(contain)
        self.setLayout(contenedor)

        self.showMaximized()
        self.show()

        
#%%
    def loadSignal(self):
        self.fSig = QFileDialog.getOpenFileName(None, 'Open file', '/home')
        if(self.fSig[0] !=''):
            self.btnLoadSig.setStyleSheet("background-color:#e8f5e9; font-size: 18px")
            names=str.split(self.fSig[0],"/")
            t=len(names)
            self.lblSignal.setText(names[t-1])
            self.btnDo.setEnabled(True)

#%%
    def enableFields(self):
        self.lblGrade.setEnabled(True)
        self.txtN.setEnabled(True)
        self.lblFcL.setEnabled(True)
        self.txtFcL.setEnabled(True)
        self.lblFcH.setEnabled(True)
        self.txtFcH.setEnabled(True)

#%%     
    def showDialog(self):
        if(self.fSig[0] !=''):
            self.plot1.clear()
            self.btnDo.setStyleSheet("background-color:#e8f5e9; font-size: 18px")
            self.fullSignal = pd.read_csv(self.fSig[0], header=None)
            self.fullSignal = self.fullSignal.as_matrix()
            self.shiftFullSignal = Operations.shiftSignal(self.fullSignal)
            Operations.noiseDelete(self.shiftFullSignal)
            
            tam = len(self.shiftFullSignal)
            
            self.shiftFullSignal = np.asarray(self.shiftFullSignal).reshape(tam,)
            self.shiftFullSignalNormal= Operations.normalSignal(self.shiftFullSignal)
            self.shiftFullSignalNormal = np.asarray(self.shiftFullSignal).reshape(tam,)

            if(self.cmbFractal.currentIndex()==0):
                self.fracta= Operations.fracTriangle(self.shiftFullSignalNormal)
            elif(self.cmbFractal.currentIndex()==1):
                self.fracta = Operations.fracSquare(self.shiftFullSignalNormal)
            elif(self.cmbFractal.currentIndex()==2):
                self.fracta = Operations.fracPenta(self.shiftFullSignalNormal)
            elif(self.cmbFractal.currentIndex()==3):
                self.fracta = Operations.fracHexa(self.shiftFullSignalNormal)
#            elif(self.cmbFractal.currentIndex()==4): #El elemento 4
#                self.fracta = Operations.fracOcta(self.shiftFullSignalNormal) #Llamar a la función que acabamos de crear
            
            if(self.checkTotalSignal.isChecked()):
                self.scaPoinc.clear()
                x, y = Operations.graphPoinc(self.shiftFullSignalNormal, self.shiftFullSignalNormal, 1)
                c1, c2 = Operations.centerPoints(self.shiftFullSignalNormal,self.shiftFullSignalNormal)
                tam = y.shape[0]
                print(x.shape)
                print(y.shape)
                spots = [{'pos': [x[i], y[i]], 'data': 1, 'brush':pg.intColor(2,3,alpha=120), 'symbol': 'o', 'size': 10} for i in range(tam)]
                spots.append({'pos': [c1, c2], 'data': 1, 'brush':pg.intColor(3,3,alpha=255), 'symbol': 'o', 'size': 10})
                self.scaPoinc.addPoints(spots)
                self.poinc.addItem(self.scaPoinc)
                sd1 = (np.std(x-y))/(np.sqrt(2))
                sd2 = (np.std(x+y))/(np.sqrt(2))
                self.txtsd1.setText(str(sd1))
                self.txtsd2.setText(str(sd2))
                self.txtc1.setText(str(c1))
                self.txtc2.setText(str(c2))
                
                fig = plt.figure()
                ax = fig.add_subplot(111, aspect='equal')
                ax.plot(x,y, 'b.', alpha=0.5, lw=2)
                ax.plot(c1,c2,'r.')
                el = Ellipse((c1, c2), sd1*2, sd2*2, fill=False, angle=-45, linewidth=1, zorder=2,color='r')
                el.set_clip_box(ax.bbox)
                ax.add_artist(el)
                sns.despine()
                
                nom = self.lblSignal.text()+'.png'
                print(nom)
                plt.savefig(nom, transparent=False)
                plt.show()

                
            self.scaInter.setData(self.fracta[:,3], self.fracta[:,4], pen=None, symbolPen='r', symbolBrush='r', symbol='o')
            self.scaInter.setSize(3)
            
            self.interFrac.addItem(self.scaInter)
            self.interFrac.addItem(self.roiInter)
            tam = len(self.shiftFullSignalNormal)
            self.timeVector = np.asarray(range(tam)).reshape(tam,)
            self.plot1.plot(self.timeVector,self.shiftFullSignalNormal,pen='k')
            
            self.btnFracInter.setEnabled(True)
   
        else:
            QMessageBox.critical(None, "Alerta","You must select a file and the channels corresponding to signal and integrated signal", QMessageBox.Ok)
            
#%%        
    def update(self):
        self.plot1.clear()
        self.plot1.plot(self.timeVector,self.shiftFullSignalNormal,pen='k')
        roiShape = self.roiInter.mapToItem(self.scaInter, self.roiInter.shape())
        selected = [pt for pt in self.scaInter.points() if roiShape.contains(pt.pos())]
        print(len(selected))
        self.inde=self.pointsInRoi(self.fracta[:,3], self.fracta[:,4],selected)
        self.plot1.plot(self.inde, self.shiftFullSignalNormal[self.inde], pen=None, symbol='o', symbolPen='m', symbolBrush='m', symbolSize=6)
        self.btnSave.setEnabled(True)
        self.btnSub.setEnabled(True)
        
#%%
    def pointsInRoi(self, fracta1, fracta2, sel):
        inde=[]
        tam=len(fracta1)
        for pt in sel:
            x=pt.pos()[0]
            y=pt.pos()[1]
            for i in range(tam):
                if((x==fracta1[i])&(y==fracta2[i])):
                    inde.append(i)
        inde=np.asarray(inde)
        return inde
    
#%%
    def saveFile(self):
        nom = QFileDialog.getSaveFileName(None, 'Saving Data in Current Plot','', '*.csv')
        tam=len(self.inde)
        arr=np.zeros((tam,1))
#        arr[:,0]=self.inde
        arr[:,0]=self.shiftFullSignalNormal[self.inde]
        df =pd.DataFrame(arr)
        df.to_csv(nom[0], index=False, mode='w', header=False)
        
#%%
    def poincSub(self):
        self.scaPoinc.clear()
        lag = int(self.txtLag.text())
        x, y = Operations.graphPoinc(self.shiftFullSignalNormal[self.inde], self.shiftFullSignalNormal[self.inde], lag)
        c1, c2 = Operations.centerPoints(self.shiftFullSignalNormal[self.inde],self.shiftFullSignalNormal[self.inde])
        tam = x.shape[0]
        spots = [{'pos': [x[i], y[i]], 'data': 1, 'brush':pg.intColor(2,3,alpha=120), 'symbol': 'o', 'size': 10} for i in range(tam)]
        spots.append({'pos': [c1, c2], 'data': 1, 'brush':pg.intColor(3,3,alpha=255), 'symbol': 'o', 'size': 10})
        self.scaPoinc.addPoints(spots)
        self.poinc.addItem(self.scaPoinc)
        sd1 = (np.std(x-y))/(np.sqrt(2))
        sd2 = (np.std(x+y))/(np.sqrt(2))
        self.txtsd1.setText(str(sd1))
        self.txtsd2.setText(str(sd2))
        self.txtc1.setText(str(c1))
        self.txtc2.setText(str(c2))
        
        fig = plt.figure()
        ax = fig.add_subplot(111, aspect='equal')
        ax.plot(x,y, 'b.', alpha=0.5, lw=2)
        ax.plot(c1,c2,'r.')
        el = Ellipse((c1, c2), sd1*2, sd2*2, fill=False, angle=-45, linewidth=1, zorder=2,color='r')
        el.set_clip_box(ax.bbox)
        ax.add_artist(el)
        sns.despine()
        
        nom = self.lblSignal.text()+'.png'
        print(nom)
        plt.savefig(nom, transparent=False)
        plt.show()

#%%     
#
if __name__=='__main__':
    app=QApplication(sys.argv)
    mw=fractalSignal()
    sys.exit(app.exec_())