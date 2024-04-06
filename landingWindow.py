import sys
import serial
import serialStuff
import serial.tools.list_ports
import graphWindow

# Error dialog stuff
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox

from PyQt6.uic import loadUi
from PyQt6 import QtWidgets, QtCore

class landingWindow(QtWidgets.QDialog):
    def __init__(self, widget=None, *args, **kwargs):
        super(landingWindow, self).__init__(*args, **kwargs)

        # Get widget from main
        self.widget = widget
        
        # Load UI from ui file
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

        # Setup serial
        ser = serialStuff.setupSerial(selectedPort, 230400)

        # Attempts to read from serial
        if(serialStuff.try_read_from_serial(ser)):
            # If it works, go to graph Window
            self.gotoGraph(ser)

        # If it doesn't work, display error dialog
        else:
            self.errorDialog("Serial port error", 
                             "ERROR: Please reconnect your upduino and try again.")
    
    """ Error dialog. Input title and message. """
    def errorDialog(self, title, msg):
        # Create the message box
        QMessageBox.critical(self, title, msg)
    
    @QtCore.pyqtSlot()
    def gotoGraph(self, ser):
        # Setup graph window
        graph_window = graphWindow.graphWindow(widget=self.widget, ser=ser)
        self.widget.addWidget(graph_window)

        # Go to graph window
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)