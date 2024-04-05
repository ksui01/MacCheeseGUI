# Child Class
from plotWidget import PlotWidget
from plotWidget2 import PlotWidget

import sys
from random import randint
import pyqtgraph as pg

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Slot
from PySide6.QtGui import QPalette, QColor

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        #Core Layouts
        mainlayout = QtWidgets.QHBoxLayout()
        plotlayout = QtWidgets.QVBoxLayout()
        sidebarlayout = QtWidgets.QVBoxLayout()
        mainlayout.addLayout(sidebarlayout)
        mainlayout.addLayout(plotlayout)

        #Plot Layouts
        topbarlayout = QtWidgets.QHBoxLayout()
        self.plotgrid = QtGui.QGridLayout()
        plotlayout.addLayout(topbarlayout)
        plotlayout.addLayout(self.plotgrid)

        
        pagelayout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()

        pagelayout.addLayout(button_layout)

        btn = QtWidgets.QPushButton("red")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("red"))

        btn = QtWidgets.QPushButton("green")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("green"))

        btn = QtWidgets.QPushButton("yellow")
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("yellow"))

        btn = QtWidgets.QPushButton("plotTest")
        btn.pressed.connect(self.plotthisstuff)
        button_layout.addWidget(btn)

        widget = QtWidgets.QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

    @QtCore.Slot()
    def plotthisstuff(self):
        self.w = PlotWidget()
        self.w.show()

    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)


    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)

class Color(QtWidgets.QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()