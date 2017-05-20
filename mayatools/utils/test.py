import sys
from PySide.QtCore import Slot
from PySide.QtGui import *

# ... insert the rest of the imports here
# Imports must precede all others ...

# Create a Qt app and a window
app = QApplication(sys.argv)

win = QWidget()
win.setWindowTitle('Test Window')
vBox = QVBoxLayout(win)
# Create a button in the window
btn = QPushButton('amol')
vBox.addWidget(btn)
pBar = QProgressBar(vBox)
vBox.addWidget(pBar)


@Slot()
def on_click():
    ''' Tell when the button is clicked. '''
    print('clicked')


@Slot()
def on_press():
    ''' Tell when the button is pressed. '''
    print('pressed')


@Slot()
def on_release():
    ''' Tell when the button is released. '''
    print('released')


# Connect the signals to the slots
btn.clicked.connect(on_click)
btn.pressed.connect(on_press)
btn.released.connect(on_release)

# Show the window and run the app
win.show()
app.exec_()