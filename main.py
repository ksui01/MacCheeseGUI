import landingWindow

import time
import sys
from random import randint


from PyQt6 import QtWidgets, QtCore



if __name__ == "__main__":

    # GUI 
    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QStackedWidget()

    # initialize the landing page
    main_window = landingWindow.landingWindow(widget=widget)
    
    # 
    widget.addWidget(main_window)
    widget.setMinimumHeight(640)
    widget.setMinimumWidth(800)

    widget.show()

    sys.exit(app.exec())