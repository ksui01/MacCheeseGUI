#Other Stuff to import
import sys
from random import randint
import pyqtgraph as pg

#Import all the PySide6 Classes
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit, 
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QPalette, QColor

#from PyQt5 import QtWidgets
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        pass
#Parent Class with PlotWidget
class PlotWidget(QtWidgets.QMainWindow):
    # Kind of like the definitions of the input and outputs, when class is called init is executed
    def __init__(self):
        super().__init__()
        # Create Widget

        # Plot settings on widget
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground("w")
        pen = pg.mkPen(color=(255, 0, 0), width=5, style=QtCore.Qt.SolidLine)
        self.plot_graph.setTitle("Signal 1 Or something", color="b", size="20pt")
        self.plot_graph.setLabel("left", "Signal Value", color="r", size="14pt")
        self.plot_graph.setLabel("bottom", "Clock Time", color="r", size="14pt")
        #self.plot_graph.setXRange(0, 40)
        self.time = list(range(10))

        temperature = [0, 1, 1, 0, 0, 1, 0, 1]
        clk = self.plotClk(temperature)
        sig = self.plotSignal(temperature)
        self.plot_graph.plot(clk, sig, pen=pen)

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
@Slot()
def say_hello():
    print("just a test")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    button1 = QPushButton("Can't think of button name")
    button1.clicked.connect(say_hello)
    button1.show()

    main = PlotWidget()
    main.resize(800, 600)
    main.show()

    sys.exit(app.exec())