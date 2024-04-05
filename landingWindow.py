import sys
import serial
import serial.tools.list_ports

from PyQt6.uic import loadUi
from PyQt6 import QtWidgets, QtCore

class landingWindow(QtWidgets.QDialog):
    def __init__(self, widget=None, *args, **kwargs):
        super(landingWindow, self).__init__(*args, **kwargs)

        # Get widget from main
        self.widget = widget

        loadUi("landingWindow.ui", self)

        # refresh COM ports
        self.refreshPorts()

        # handles click on Start button
        self.startButton.clicked.connect(self.startClicked)
    
    """Refreshes the list of serial ports."""
    def refreshPorts(self):
        
        self.portComboBox.clear()
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            self.portComboBox.addItem(port, desc)

    """Handler for the start button click event."""
    def startClicked(self):
        selectedPort = self.portComboBox.currentText()
        # Print selected port
        print(f"Selected port: {selectedPort}")

        # goes to graph Window
        self.gotoGraph()
    
    @QtCore.pyqtSlot()
    def gotoGraph(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)