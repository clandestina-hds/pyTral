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
from PyQt5.QtWidgets import (QApplication, QPushButton, QSplitter, QFileDialog, QMessageBox, QLabel, QComboBox,QWidget, QCheckBox)
from PyQt5.QtCore import Qt
import pyqtgraph as pg 
from Operations import Operations
import numpy as np
import pandas as pd

#%%
class fractalSignal(QWidget):
    def __init__(self):
        super(fractalSignal,self).__init__()
        self.initUI()

#%% 
    def initUI(self):
        pg.setConfigOption('background', 'w')
        self.fullSignal=[]
        self.shiftFullSignal=[]
        self.shiftFullSignalNormal=[]
        
        self.fSig=''
        
        contenedor=QtWidgets.QHBoxLayout(self)
        
        contain=QSplitter(Qt.Horizontal)

        buttons = QtWidgets.QVBoxLayout()
        graphics = QtWidgets.QVBoxLayout()
        imaFrac = QtWidgets.QHBoxLayout()
       
        self.btnLoadSig = QPushButton('Load Signal')
        self.btnLoadSig.clicked.connect(self.loadSignal)
        self.btnLoadSig.setStyleSheet("background-color:#fbe9e7")
        
        self.lblSignal = QLabel('')
        
        self.checkTotalSignal = QCheckBox('Signal', self)
        

        self.cmbFractal = QComboBox()
        self.cmbFractal.setStyleSheet("background-color:#fbe9e7")
        self.cmbFractal.addItem("Triangle") #Elemento 0
        self.cmbFractal.addItem("Square") #Elemento 1
        self.cmbFractal.addItem("Pentagon") #Elemento 2
        self.cmbFractal.addItem("Hexagon") #Elemento 3
        #self.cmbFractal.addItem("Octgon") #Ahora éste es el elemento 4
        
        self.btnDo = QPushButton("Do Fractal")
        self.btnDo.setDisabled(True)
        self.btnDo.clicked.connect(self.showDialog)

        self.btnFracInter = QPushButton("Points-Inter")
        self.btnFracInter.setDisabled(True)
        self.btnFracInter.clicked.connect(self.update)
        
        self.btnSub = QPushButton("Graph Poincare")
        self.btnSub.setDisabled(True)
        self.btnSub.clicked.connect(self.poincSub)
        
        self.btnSave = QPushButton("Save Current Data")
        self.btnSave.setDisabled(True)
        self.btnSave.clicked.connect(self.saveFile)
        
        self.viewBox=pg.GraphicsLayoutWidget()
        self.interFrac = self.viewBox.addViewBox(row=0, col=0, lockAspect=True)
        self.poinc = self.viewBox.addViewBox(row=0, col=1, lockAspect=True)
        
        self.scaInter=pg.ScatterPlotItem()
        self.scaPoinc=pg.ScatterPlotItem()

        self.roiInter=pg.PolyLineROI([[0.2, 0.5], [0.8, 0.5], [0.5, 0]], pen=(6,9), closed=True)

        imaFrac.addWidget(self.viewBox)

        buttons.setSizeConstraint(0)
        
        buttons.addWidget(self.btnLoadSig)
        buttons.addWidget(self.lblSignal)
        
        buttons.addWidget(self.checkTotalSignal)
        
        buttons.addWidget(QLabel("Fractal Type"))
        buttons.addWidget(self.cmbFractal)
        
        buttons.addWidget(self.btnDo)
        buttons.addWidget(self.btnFracInter)
        buttons.addWidget(self.btnSub)
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
            self.btnLoadSig.setStyleSheet("background-color:#e8f5e9")
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
            self.btnDo.setStyleSheet("background-color:#e8f5e9")
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
                x, y = Operations.graphPoinc(self.shiftFullSignalNormal)
                self.scaPoinc.setData(x, y, pen=None, symbolPen='r', symbolBrush='r', symbol='o')
                self.scaPoinc.setSize(2)
                self.poinc.addItem(self.scaPoinc)
                
            self.scaInter.setData(self.fracta[:,3], self.fracta[:,4], pen=None, symbolPen='r', symbolBrush='r', symbol='o')
            self.scaInter.setSize(2)
            
            self.interFrac.addItem(self.scaInter)
            self.interFrac.addItem(self.roiInter)
            
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
        arr=np.zeros((tam,2))
        arr[:,0]=self.inde
        arr[:,1]=self.shiftFullSignalNormal[self.inde]
        df =pd.DataFrame(arr)
        df.to_csv(nom[0], index=False, mode='w', header=False)
        
#%%
    def poincSub(self):
        x, y = Operations.graphPoinc(self.inde)
        self.scaPoinc.setData(x, y, pen=None, symbolPen='r', symbolBrush='r', symbol='o')
        self.scaPoinc.setSize(2)
        self.poinc.addItem(self.scaPoinc)

#%%     
#
if __name__=='__main__':
    app=QApplication(sys.argv)
    mw=fractalSignal()
    sys.exit(app.exec_())