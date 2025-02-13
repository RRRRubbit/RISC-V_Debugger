from PyQt5 import QtWidgets
from LOGIC.mainwindow import *
#from LOGIC.BreakPointDialog import *
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec_())