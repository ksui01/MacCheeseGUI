import time
import serialStuff
import resourcePath
from random import randint

from PyQt6.QtWidgets import QMessageBox

from PyQt6.uic import loadUi
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QTimer

import pyqtgraph as pg
from pyqtgraph import InfiniteLine, TextItem, LinearRegionItem



class graphWindow(QtWidgets.QMainWindow):
  def __init__(self, widget=None, selectedPort=None, *args, **kwargs):
    super(graphWindow, self).__init__(*args, **kwargs)

    #loadUi("biggraphwindow.ui", self)
    PATH = resourcePath.resource_path("bigGraphWindow.ui")
    loadUi(PATH, self)

    # Set the widget
    self.widget = widget 

    # Get the selected port
    self.selectedPort = selectedPort

    # Initialize the arrays for graphs
    self.psigs = [[] for _ in range(8)]  # List to hold 8 signal arrays

    # State of the graph (paused or not)
    self.paused = False 
    self.initialized = False

    # Start plotting from index 0
    self.x = 0

    # Print message to user
    self.consoleLog("Press start to begin!")

    # Setup buttons
    self.backButton.clicked.connect(self.gotoLandingPage)
    self.playButton.clicked.connect(self.startClicked)
    #self.pauseButton.clicked.connect(self.pauseFun)
    self.stopButton.clicked.connect(self.stopFun)

  ''' Stop the simulation '''
  def stopFun(self):
    self.consoleLog("Plotting stopped.")

    # Set to paused
    self.paused = True

    # Send a serial signal "S"
    self.ser.write(b"Q")

  ''' Pauses the simulation '''
  # def pauseFun(self):
  #   self.pause = True
  #   print(f"Setting pause to {self.pause}")

  ''' Unpauses the simulation '''
  # def unpauseFun(self):
  #   print("Unpausing")
  #   self.pause = False

  ''' Display messages to user in a box in the GUI. '''
  def consoleLog(self, msg):
    self.console.setText(msg)

  """Handler for the start button click event."""
  def startClicked(self):
      self.consoleLog("Starting plots...")

      # Set pause False
      self.paused = False

      # Cleanup arrays
      for i in range(8):
        self.psigs[i].clear()

      # Setup serial
      self.ser = serialStuff.setupSerial(self.selectedPort, 230400)

      # Send a serial signal "S"
      self.ser.write(b"S")

      # Wait 3s
      time.sleep(3)

      # Initialize graphs if they haven't been initialized already
      if (self.initialized == False):
        self.initializeGraphs()
  
  """ Error dialog. Input title and message. """
  def errorDialog(self, title, msg):
      # Create the message box
      QMessageBox.critical(self, title, msg)

  def updateData(self):
    if (self.paused == False):
      self.consoleLog("Reading...")

      self.psigs = serialStuff.updateArrays(self.ser, *self.psigs)
      
      
      # Automatically stop plotting if too many numbers
      if (len(self.psigs[0]) > 100000):
        print("Array is too big. Stopping.")
        self.stopFun()

      
      # Vertical offset 
      offset = 2.05

      for i, plot in enumerate(self.plots):
        offset_data = [y + i * offset for y in self.psigs[i]]
        plot.setData(offset_data)  # Update each plot with new data

  
  @QtCore.pyqtSlot()
  def gotoLandingPage(self):
    # Stop the simulation
    self.stopFun()

    # Go back to landing page
    self.widget.setCurrentIndex(self.widget.currentIndex() - 1)

  # Sets the serial port this graph is reading from.
  def setSerialPort(self, ser):
    self.ser = ser

  ''' Initialize graphs'''
  def initializeGraphs(self):
    print("Initializing graphs")

    # Set to initialized
    self.initialized = True

    # Initialize timer for graph
    self.timer = QTimer()
    self.timer.timeout.connect(self.updateData)
    self.timer.start(10) # adjust interval

    # Track horizontal lines and clicks
    self.click_count = 0
    self.lines = []

    # Colors
    self.pens = [
      pg.mkPen(color=(0, 255, 255), width=2),
      pg.mkPen(color=(255, 0, 255), width=2),
      pg.mkPen(color=(127, 0, 255), width=2),
      pg.mkPen(color=(0, 0, 255), width=2),
      pg.mkPen(color=(0, 255, 0), width=2),
      pg.mkPen(color=(255, 255, 0), width=2),
      pg.mkPen(color=(255, 128, 0), width=2),
      pg.mkPen(color=(255, 0, 0), width=2)
    ]

    # Initialize plots for each signal
    self.plots = [self.biggraph.plot(pen=self.pens[i]) for i in range(8)]
    self.biggraph.setRange(yRange=[0, 15])
    self.biggraph.showGrid(x=True, y=False)

    # Remove the tick labels of y-axis
    y_axis = self.biggraph.getAxis('left')
    y_axis.setStyle(tickTextOffset=0)
    y_axis.setTicks([]) 

    # Disable y-axis changing from scrolling
    view_box = self.biggraph.getViewBox()
    view_box.setMouseEnabled(x=True, y=False)

    # Adding a vertical line following the cursor
    self.vLine = InfiniteLine(angle=90, movable=False)  # Vertical line
    self.textItem = TextItem(anchor=(0,1))  # Text item for displaying the value
    self.biggraph.addItem(self.vLine, ignoreBounds=True)  # Add vertical line to the plot
    self.biggraph.addItem(self.textItem)  # Add text item to the plot

    # Handling mouse movement and clicks
    #self.proxyClick = pg.SignalProxy(self.biggraph.scene().sigMouseClicked, rateLimit=60, slot=self.onClick)
    self.biggraph.scene().sigMouseClicked.connect(self.mouseClicked)
    self.proxy = pg.SignalProxy(self.biggraph.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

  ''' Handle a mousle clicked on the big graph.'''
  def mouseClicked(self, event):
    pos = event.scenePos()
    if self.biggraph.sceneBoundingRect().contains(pos):
      mousePoint = self.biggraph.plotItem.vb.mapSceneToView(pos)
      self.addVerticalLine(mousePoint.x())

  def addVerticalLine(self, x):
    # First click - add the first line
    if self.click_count == 0:
      self.firstLine = InfiniteLine(angle=90, movable=False, pos=x)
      self.biggraph.addItem(self.firstLine, ignoreBounds=True)
      self.click_count = 1

    # Second click - add the second line
    elif self.click_count == 1:
      self.secondLine = InfiniteLine(angle=90, movable=False, pos=x)
      self.biggraph.addItem(self.secondLine, ignoreBounds=True)
      self.click_count = 2

      # Highlight the area between the lines
      self.region = LinearRegionItem(values=(self.firstLine.value(), self.secondLine.value()), movable=False)
      self.biggraph.addItem(self.region, ignoreBounds=True)

      # Calculate and print the difference
      difference = abs(self.secondLine.value() - self.firstLine.value())
      diff_round = round(difference, 2) # round it to 2
      self.y_delta_val.setText(str(diff_round))

    # Third click, reset 
    elif self.click_count == 2:
      self.biggraph.removeItem(self.firstLine)
      self.biggraph.removeItem(self.secondLine)
      self.biggraph.removeItem(self.region)
      self.y_delta_val.setText("")
      self.click_count = 0
    
    
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
  
  ''' Handles mouse movement for vertical line '''
  def mouseMoved(self, evt):
    pos = evt[0]  # Extract mouse position
    if self.biggraph.sceneBoundingRect().contains(pos):
      mousePoint = self.biggraph.plotItem.vb.mapSceneToView(pos)
      self.vLine.setPos(mousePoint.x())  # Update the vertical line position
      
      # Get the signal values at this x position
      x_val, y_signal_values = self.getSignalValueAt(mousePoint.x())
      
      # Display the signal values in the GUI
      self.displayGraphValues(x_val, y_signal_values)

  ''' Returns x coordinate and an array with y signal values at coordinate x. 
  If it's out of bonds, returns an empty array. '''
  def getSignalValueAt(self, x):
    # Implement logic to find and return the signal value at or nearest to x
    idx = int(x)  # Convert x to an index

    y_signal_values = []

    if 0 <= idx < len(self.psigs[0]):
      for signal in self.psigs:
        # Append the y-value at idx from each signal
        y_signal_values.append(signal[idx])

    #print(y_signal_values)
    return idx, y_signal_values
  
  ''' Sets the y values text box to the provided signal values.'''
  def displayGraphValues(self, x, y_signal_values):
    # Define the colors for each y-value
    colors = [
        (0, 255, 255),
        (255, 0, 255),
        (127, 0, 255),
        (0, 0, 255),
        (0, 255, 0),
        (255, 255, 0),
        (255, 128, 0),
        (255, 0, 0)
    ]
    
    # HTML string with y-values in their respective colors
    y_values_html = ''.join(f'<span style="color: rgb{colors[i]};">{y}</span>, '
                            for i, y in enumerate(y_signal_values))
    
    # Trim the trailing comma and space
    y_values_html = y_values_html.rstrip(', ')

    # Set the QLabel text
    self.y_val.setText(y_values_html)
    self.x_val.setText(str(x))
  

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