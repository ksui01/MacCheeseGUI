import serialStuff
import landingWindow
import graphWindow

import time
import sys
from random import randint


from PyQt6 import QtWidgets, QtCore



if __name__ == "__main__":

    # # Setup serial
    # ser = serialStuff.setupSerial('COM12', 38400); 

    # # loop for 10s
    # start_time = time.time()
    # duration = 5
    # while (time.time() - start_time) < duration:
    #     # Update arrays
    #     psig1, psig2, psig3, psig4, psig5, psig6, psig7, psig8 = serialStuff.updateArrays(ser, psig1, psig2, psig3, psig4, psig5, psig6, psig7, psig8)

    # GUI 
    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QStackedWidget()

    # initialize the other windows
    main_window = landingWindow.landingWindow(widget=widget)
    graph_window = graphWindow.graphWindow()

    # 
    widget.addWidget(main_window)
    widget.addWidget(graph_window)
    widget.setFixedHeight(640)
    widget.setFixedWidth(800)

    widget.show()

    sys.exit(app.exec())