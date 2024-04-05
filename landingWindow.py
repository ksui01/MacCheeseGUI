import sys
import serial
import serial.tools.list_ports
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets, QtCore

class landingWindow(QtWidgets.QDialog):
    def __init__(self):
        super(landingWindow, self).__init__()
        loadUi("landingWindow.ui", self)
        self.pushButton.clicked.connect(self.gotoGraph)
        
    @QtCore.pyqtSlot()
    def gotoGraph(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)