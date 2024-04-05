import serialStuff
import time

import sys
from random import randint
import pyqtgraph as pg

from PyQt6.uic import loadUi
from PyQt6 import QtWidgets, QtCore

# Signal arrays
psig1 = []
psig2 = []
psig3 = []
psig4 = []
psig5 = []
psig6 = []
psig7 = []
psig8 = []

class ReadMe(QtWidgets.QDialog):
    def __init__(self):
        super(ReadMe, self).__init__()
        loadUi("READMEwindow.ui", self)
        self.pushButton.clicked.connect(self.gotoGraph)
        
    @QtCore.pyqtSlot()
    def gotoGraph(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

class GraphWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("biggraphwindow.ui", self)
        self.pushButton.clicked.connect(self.gotoReadMe)

        #graph settings
        self.initializeGraphs()

    @QtCore.pyqtSlot()
    def gotoReadMe(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)

    # This is supposed to update the graph at each additional cycle. In theory
    def updateGraphs(self, psig1, psig2, psig3, psig4, psig5, psig6, psig7, psig8):
        pass

    def initializeGraphs(self):
        #self.biggraph.setBackground("w")

        RedPen = pg.mkPen(color=(255, 0, 0), width=2)
        OrangePen = pg.mkPen(color=(255, 128, 0), width=2)
        YellowPen = pg.mkPen(color=(255, 255, 0), width=2)
        GreenPen = pg.mkPen(color=(0, 255, 0), width=2)
        BluePen = pg.mkPen(color=(0, 0, 255), width=2)
        PurplePen = pg.mkPen(color=(127, 0, 255), width=2)
        PinkPen = pg.mkPen(color=(255, 0, 255), width=2)
        CyanPen = pg.mkPen(color=(0, 255, 255), width=2)

        

        # for i in range(50):
        #     psig1.append(randint(0, 1))
        #     psig2.append(randint(0, 1))
        #     psig3.append(randint(0, 1))
        #     psig4.append(randint(0, 1))
        #     psig5.append(randint(0, 1))
        #     psig6.append(randint(0, 1))
        #     psig7.append(randint(0, 1))
        #     psig8.append(randint(0, 1))

        self.time = list(range(10))

        clk = self.plotClk(psig1)
        sig = self.plotSignal(psig1)
        self.biggraph.plot(clk, sig, pen=PurplePen)

        clk = self.plotClk(psig2)
        sig = self.plotSignal(psig2)
        sig = self.plotBig(sig, 7)
        self.biggraph.plot(clk, sig, pen=PinkPen)

        clk = self.plotClk(psig3)
        sig = self.plotSignal(psig3)
        sig = self.plotBig(sig, 6)
        self.biggraph.plot(clk, sig, pen=GreenPen)

        clk = self.plotClk(psig4)
        sig = self.plotSignal(psig4)
        sig = self.plotBig(sig, 5)
        self.biggraph.plot(clk, sig, pen=OrangePen)

        clk = self.plotClk(psig5)
        sig = self.plotSignal(psig5)
        sig = self.plotBig(sig, 4)
        self.biggraph.plot(clk, sig, pen=CyanPen)

        clk = self.plotClk(psig6)
        sig = self.plotSignal(psig6)
        sig = self.plotBig(sig, 3)
        self.biggraph.plot(clk, sig, pen=YellowPen)
        
        clk = self.plotClk(psig7)
        sig = self.plotSignal(psig7)
        sig = self.plotBig(sig, 2)
        self.biggraph.plot(clk, sig, pen=BluePen)

        clk = self.plotClk(psig8)
        sig = self.plotSignal(psig8)
        sig = self.plotBig(sig, 1)
        self.biggraph.plot(clk, sig, pen=RedPen)

        self.biggraph.setRange(yRange=[1,15])
        self.biggraph.showGrid(x=True, y=False)
        
    #Plots the 8 graphs according to where they should be located
    #The value inserted should be which graph to plot and what to plot
    #Should be used after plotSignal
    def plotBig(self, sigVal, sigNum):
        bigVal = []
        #Theres a more efficient way to do this but I don't want to think
        for i in range(len(sigVal)):
            if (sigNum == 8):
                return sigVal
            elif (sigNum == 7):
                bigVal.append(int(sigVal[i]) + (2 * 1))
            elif (sigNum == 6):
                bigVal.append(int(sigVal[i]) + (2 * 2))
            elif (sigNum == 5):
                bigVal.append(int(sigVal[i]) + (2 * 3))
            elif (sigNum == 4):
                bigVal.append(int(sigVal[i]) + (2 * 4))
            elif (sigNum == 3):
                bigVal.append(int(sigVal[i]) + (2 * 5))
            elif (sigNum == 2):
                bigVal.append(int(sigVal[i]) + (2 * 6))
            elif (sigNum == 1):
                bigVal.append(int(sigVal[i]) + (2 * 7))
        return bigVal

    #Plots the graphs such that it makes square waves
    #Returns an array of time (clk) that goes along displayed signal
    def plotClk(self, sigVal):
        t = 0
        timeVal = []
        prevSigVal = sigVal[0]
        for i in range(len(sigVal)):
            currSigVal = sigVal[i]
            if (i == 0):
                timeVal.append(t)
            elif (prevSigVal == currSigVal):
                t = t + 1
                timeVal.append(t)
            else:
                t = t + 1
                timeVal.append(t)
                timeVal.append(t)
            if (i == len(sigVal) - 1):
                t = t + 1
                timeVal.append(t)
            prevSigVal = sigVal[i]
        return timeVal

    #Plots the graphs such that it makes square waves
    #Returns an array of signals (0 or 1) that goes along displayed signal
    def plotSignal(self, sigVal):
        newSigVal = []
        prevSigVal = sigVal[0]
        for i in range(len(sigVal)):
            currSigVal = sigVal[i]
            if (i == 0):
                newSigVal.append(sigVal[i])
            elif (prevSigVal == currSigVal):
                newSigVal.append(sigVal[i])
            else:
                newSigVal.append(sigVal[i - 1])
                newSigVal.append(sigVal[i])
            if (i == len(sigVal) - 1):
                newSigVal.append(sigVal[i])
            prevSigVal = sigVal[i]
        return newSigVal
    
    # Gets the number of plot flips there are
    # Was gonna use it but is kinda pointless right now
    def flips(self, val):
        numflip = 0
        prev = val[0]
        for i in range(len(val)):
            curr = val[i]
            if (prev != curr):
                numflip = numflip + 1
            prev = curr
        return numflip

if __name__ == "__main__":

    # Setup serial
    ser = serialStuff.setupSerial('COM12', 38400); 

    # loop for 10s
    start_time = time.time()
    duration = 5
    while (time.time() - start_time) < duration:
        # Update arrays
        psig1, psig2, psig3, psig4, psig5, psig6, psig7, psig8 = serialStuff.updateArrays(ser, psig1, psig2, psig3, psig4, psig5, psig6, psig7, psig8)

    # GUI 
    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QStackedWidget()

    main_window = ReadMe()
    graph_window = GraphWindow()
    widget.addWidget(main_window)
    widget.addWidget(graph_window)
    widget.setFixedHeight(640)
    widget.setFixedWidth(800)

    widget.show()

    sys.exit(app.exec())