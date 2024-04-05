import sys
from random import randint
import pyqtgraph as pg

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Slot
from PySide6.QtGui import QPalette, QColor

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Core Customization features
        self.setWindowTitle("My App")
        self.setFixedWidth(400)
        self.setFixedHeight(600)

        #Core Layouts
        mainlayout = QtWidgets.QHBoxLayout()
        plotlayout = QtWidgets.QVBoxLayout()
        sidebarlayout = QtWidgets.QVBoxLayout()
        mainlayout.addLayout(sidebarlayout)
        mainlayout.addLayout(plotlayout)

        #Plot Layouts
        topbarlayout = QtWidgets.QHBoxLayout()
        self.plotgrid = QtWidgets.QGridLayout()
        plotlayout.addLayout(topbarlayout)
        plotlayout.addLayout(self.plotgrid)

        #Initialize the plots
        #self.w1 = PlotWidget()
        #self.w2 = PlotWidget()
        #self.w3 = PlotWidget()

        #Add the plots in
        #self.plotgrid.addLayout(self.w1)
        #self.plotgrid.addLayout(self.w2)
        #self.plotgrid.addLayout(self.w3)


        #Adding topbar layout buttons
        btn = QtWidgets.QPushButton("temp1")
        btn.pressed.connect(self.temp1)
        topbarlayout.addWidget(btn)

        btn = QtWidgets.QPushButton("temp2")
        btn.pressed.connect(self.temp2)
        topbarlayout.addWidget(btn)

        btn = QtWidgets.QPushButton("temp3")
        btn.pressed.connect(self.temp3)
        topbarlayout.addWidget(btn)

        #Adding sidebar layout buttons
        btn = QtWidgets.QPushButton("side1")
        btn.pressed.connect(self.temp1)
        sidebarlayout.addWidget(btn)

        btn = QtWidgets.QPushButton("side2")
        btn.pressed.connect(self.temp2)
        sidebarlayout.addWidget(btn)

        btn = QtWidgets.QPushButton("side3")
        btn.pressed.connect(self.temp3)
        sidebarlayout.addWidget(btn)

        btn = QtWidgets.QPushButton("plotTest")
        btn.pressed.connect(self.plotthisstuff)
        topbarlayout.addWidget(btn)

        widget = QtWidgets.QWidget()
        widget.setLayout(mainlayout)
        self.setCentralWidget(widget)

    @QtCore.Slot()
    def temp1(self):
        pass

    @QtCore.Slot()
    def temp2(self):
        pass

    @QtCore.Slot()
    def temp3(self):
        pass

    @QtCore.Slot()
    def plotthisstuff(self):
        self.w = PlotWidget()
        self.w.show()


class Color(QtWidgets.QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class PlotWidget(QtWidgets.QWidget):
    # Kind of like the definitions of the input and outputs, when class is called init is executed
    def __init__(self):
        super().__init__()
        #Some inital variables
        plotnumber = 1

        #setting the correct window titles
        self.setWindowTitle("Plot "+ str(plotnumber))

        #fucking around with layout components
        self.plot_graph = pg.PlotWidget()
        self.time = list(range(10))
        self.label = QtWidgets.QLabel("Plot Window")

        #Plot graph settings
        self.plot_graph.setBackground("w")
        self.plot_graph.setBackground("w")
        self.plot_graph.setTitle("Signal 1 Or something", color="b", size="20pt")
        self.plot_graph.setLabel("left", "Signal Value", color="r", size="14pt")
        self.plot_graph.setLabel("bottom", "Clock Time", color="r", size="14pt")
        #self.plot_graph.setXRange(0, 40)

        # Just going to henry-fy it aka, make it look nice
        thickRedPen = pg.mkPen(color=(255, 0, 0), width=5, style=QtCore.Qt.SolidLine)

        #The actual plotting of the graph
        temperature = [0, 1, 1, 0, 0, 1, 0, 1]
        clk = self.plotClk(temperature)
        sig = self.plotSignal(temperature)
        self.plot_graph.plot(clk, sig, pen=thickRedPen)

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

    window = MainWindow()
    window.show()

    sys.exit(app.exec())