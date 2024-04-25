# MacCheeseGUI
Tufts Senior Design Project: FPGA Logic Analyzer
Written in Python using PyQt6. 

# How to run it:
1. Make sure you are using Python 3.10.13
  Run "python --version" to make sure.

2. Create a new environment:
  python -m venv venv

3. Activate environment
  source venv/bin/activate (macOS)
  \venv\Scripts\activate (windows)

4. Install dependencies: 
  pip install -r requirements.txt

5. Run the program: 
  python main.py 

# How to transform into an executable (macOS):
pyinstaller --windowed \
            --distpath DIST\
            --workpath WORK \
            --add-data "biggraphwindow.ui:." \
            --add-data "landingWindow.ui:." \
            --add-data "background.png:." \
            main.py

# Important libraries:
pip install pyqt6-tools # tool to edit .ui files. run in terminal: pyqt6-tools designer
pip install pyinstaller # used to convert into an .exe file (we are using Python 3.10.13)
pip install pyqt6==6.6.1
pip install PyQt6-Qt6==6.6.3
pip install pyqtgraph==0.13.4
pip install pyserial==3.5


