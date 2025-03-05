from PyQt5.QtCore import pyqtSignal

from GUI.ui_memory_widget import *
from GUI.ui_MainWindow import *

class Memorywidget(QtWidgets.QDialog, Ui_Memory_widget):
    signal_memory_size = pyqtSignal(int)
    siganl_memory_model = pyqtSignal(str)
    signal_memory_start = pyqtSignal(int)
    def __init__(self, parent=None):
        super(Memorywidget, self).__init__(parent)
        self.setupUi(self)
        # 设置实例
        self.CreateItems()
        # 设置信号与槽
        self.CreateSignalSlot()
       # self.cleanAllBreakPoints()

    def CreateItems(self):
        return

    def CreateSignalSlot(self):
        self.pushButton_size_set.clicked.connect(self.memory_size_change)
        self.pushButton_size_set.clicked.connect(self.memory_address_start_change)
        return
    # 槽函数
    def memory_address_start_change(self):
        self.signal_memory_start.emit(self.lineEdit_memaddr_start.text)
    def memory_size_change(self):
        match self.comboBox_memorysize.currentIndex():
            case 0:
                self.signal_memory_size.emit(60)
                print(0)
            case 1:
                self.signal_memory_size.emit(252)
                print(1)
    def memory_model_change(self):
        match self.comboBox_memorymodel.currentIndex():
            case 0:
                self.siganl_memory_model.emit('IMEM')
                print(0)
            case 1:
                self.siganl_memory_model.emit('DMEM')
                print(1)
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Memorywidget()
    mainWindow.show()
    sys.exit(app.exec_())