import resourcePath
import serial
import serialStuff
import serial.tools.list_ports
import graphWindow

from PyQt6.QtWidgets import QMessageBox
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QPixmap

class landingWindow(QtWidgets.QDialog):
    def __init__(self, widget=None, *args, **kwargs):
        super(landingWindow, self).__init__(*args, **kwargs)

        # Get widget from main
        self.widget = widget
        
        # Load UI from ui file
        PATH = resourcePath.resource_path("landingWindow.ui")
        loadUi(PATH, self)

        # refresh COM ports
        self.refreshPorts()

        # loads background image
        image_path = resourcePath.resource_path("background.png")
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.background.setPixmap(pixmap)

        # handles click on Start button
        self.startButton.clicked.connect(self.startClicked)
        self.refreshButton.clicked.connect(self.refreshPorts)

    
    
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

        if(serialStuff.check_serial_port(selectedPort)):
            self.gotoGraph(selectedPort)
        else:
            self.errorDialog("Serial port error", 
                        "Please select a valid serial port.")

    
    """ Error dialog. Input title and message. """
    def errorDialog(self, title, msg):
        # Create the message box
        QMessageBox.critical(self, title, msg)
    
    @QtCore.pyqtSlot()
    def gotoGraph(self, selectedPort):
        # Setup graph window
        graph_window = graphWindow.graphWindow(widget=self.widget, selectedPort=selectedPort)
        self.widget.addWidget(graph_window)

        # Go to graph window
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)