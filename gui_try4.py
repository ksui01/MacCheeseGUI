import sys
from random import randint
import pyqtgraph as pg

from PyQt6.uic import loadUi
from PyQt6 import QtWidgets, QtCore

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
        loadUi("graphwindow.ui", self)
        self.pushButton.clicked.connect(self.gotoReadMe)

        #graph settings
        self.initializeGraphs()

    @QtCore.pyqtSlot()
    def gotoReadMe(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)

    def initializeGraphs(self):
        self.graph1.setBackground("w")
        self.graph2.setBackground("w")
        self.graph3.setBackground("w")
        self.graph4.setBackground("w")
        self.graph5.setBackground("w")
        self.graph6.setBackground("w")
        self.graph7.setBackground("w")
        self.graph8.setBackground("w")

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