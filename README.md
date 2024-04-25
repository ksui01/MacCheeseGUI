# MacCheeseGUI
Tufts Senior Design Project: FPGA Logic Analyzer. <br>
Written in Python using PyQt6. 

# Downloads
MacOS: https://drive.google.com/file/d/16-QHJ66DIr_bPqAezycqFF1WI-qpUUme/view?usp=sharing
Windows: 

# How to run source code:
1. Make sure you are using Python 3.10.13 <br>
  Run "python --version" to make sure.

2. Create a new environment: <br>
  python -m venv venv <br>

3. Activate environment: <br>
  source venv/bin/activate (macOS) <br>
  \venv\Scripts\activate (windows) <br>

4. Install dependencies:  <br>
  pip install -r requirements.txt <br>

5. Run the program:  <br>
  python main.py  <br>

# How to transform into an executable (macOS): <br>
pyinstaller --windowed \
            --distpath DIST\
            --workpath WORK \
            --add-data "biggraphwindow.ui:." \
            --add-data "landingWindow.ui:." \
            --add-data "background.png:." \
            main.py

# Important libraries: <br>
pip install pyqt6-tools # tool to edit .ui files. run in terminal: pyqt6-tools designer <br>
pip install pyinstaller # used to convert into an .exe file (we are using Python 3.10.13) <br>
pip install pyqt6==6.6.1 <br>
pip install PyQt6-Qt6==6.6.3 <br>
pip install pyqtgraph==0.13.4 <br>
pip install pyserial==3.5 <br>


