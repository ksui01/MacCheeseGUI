import time
import serialStuff
import serial.tools.list_ports
from random import randint

from PyQt6.uic import loadUi
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QTimer

import pyqtgraph as pg

class graphWindow(QtWidgets.QMainWindow):
  def __init__(self, widget=None, ser=None, *args, **kwargs):
    super(graphWindow, self).__init__(*args, **kwargs)

    # Set the widget
    self.widget = widget 

    # Set the serial port
    self.ser = ser

    # Initialize timer for graph
    self.timer = QTimer()
    self.timer.timeout.connect(self.updateData)
    self.timer.start(100) # adjust interval

    loadUi("biggraphwindow.ui", self)
    self.pushButton.clicked.connect(self.gotoLandingPage)
 
    #graph settings
    self.initializeGraphs()
  def updateData(self):
    # Assuming updateArrays and readByteFromSerial are defined elsewhere
    self.psigs = serialStuff.updateArrays(self.ser, *self.psigs)
    
    # Limit the size of each array to the last 200 data points
    self.psigs = [psig[-200:] for psig in self.psigs]  # Trim each array
    
    # Vertical offset 
    offset = 2

    for i, plot in enumerate(self.plots):
      offset_data = [y + i * offset for y in self.psigs[i]]
      plot.setData(offset_data)  # Update each plot with new data
  
  @QtCore.pyqtSlot()
  def gotoLandingPage(self):
    self.widget.setCurrentIndex(self.widget.currentIndex() - 1)

  # Sets the serial port this graph is reading from.
  def setSerialPort(ser):
    self.ser = ser

  # This is supposed to update the graph at each additional cycle. In theory
  def updateGraphs(self, psig1, psig2, psig3, psig4, psig5, psig6, psig7, psig8):
    pass

  ''' Initialize graphs'''
  def initializeGraphs(self):
    self.psigs = [[] for _ in range(8)]  # List to hold 8 signal arrays
    self.pens = [
      pg.mkPen(color=(255, 0, 0), width=2),
      pg.mkPen(color=(255, 128, 0), width=2),
      pg.mkPen(color=(255, 255, 0), width=2),
      pg.mkPen(color=(0, 255, 0), width=2),
      pg.mkPen(color=(0, 0, 255), width=2),
      pg.mkPen(color=(127, 0, 255), width=2),
      pg.mkPen(color=(255, 0, 255), width=2),
      pg.mkPen(color=(0, 255, 255), width=2)
    ]
    # Initialize plots for each signal
    self.plots = [self.biggraph.plot(pen=self.pens[i]) for i in range(8)]
    self.biggraph.setRange(yRange=[1, 15])
    self.biggraph.showGrid(x=True, y=False)

    # Remove the tick labels of y-axis
    y_axis = self.biggraph.getAxis('left')
    y_axis.setStyle(tickTextOffset=0)
    y_axis.setTicks([]) 

    # Disable y-axis changing from scrolling
    view_box = self.biggraph.getViewBox()
    view_box.setMouseEnabled(x=True, y=False)
    
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
  

  '''Initialize graphs with placeholders'''
  def initializeGraphsPlaceholder(self):
    #self.biggraph.setBackground("w")

    RedPen = pg.mkPen(color=(255, 0, 0), width=2)
    OrangePen = pg.mkPen(color=(255, 128, 0), width=2)
    YellowPen = pg.mkPen(color=(255, 255, 0), width=2)
    GreenPen = pg.mkPen(color=(0, 255, 0), width=2)
    BluePen = pg.mkPen(color=(0, 0, 255), width=2)
    PurplePen = pg.mkPen(color=(127, 0, 255), width=2)
    PinkPen = pg.mkPen(color=(255, 0, 255), width=2)
    CyanPen = pg.mkPen(color=(0, 255, 255), width=2)

    

    for i in range(50):
      psig1.append(randint(0, 1))
      psig2.append(randint(0, 1))
      psig3.append(randint(0, 1))
      psig4.append(randint(0, 1))
      psig5.append(randint(0, 1))
      psig6.append(randint(0, 1))
      psig7.append(randint(0, 1))
      psig8.append(randint(0, 1))

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