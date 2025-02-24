from PyQt5.QtCore import pyqtSignal

from GUI.setting import *
from GUI.ui_MainWindow import *

class SettingDialog(QtWidgets.QDialog, Ui_Setting):
    signal_update_csr_option=pyqtSignal(list)

    def __init__(self, parent=None):
        super(SettingDialog, self).__init__(parent)
        self.setupUi(self)
        # 设置实例
        self.CreateItems()
        # 设置信号与槽
        self.CreateSignalSlot()
       # self.cleanAllBreakPoints()

    def CreateItems(self):
        return

    def CreateSignalSlot(self):
        self.buttonBox.accepted.connect(self.run_option)
        return
    # 槽函数
    def run_option(self):
        s_1=self.checkBox.isChecked()
        s_2=self.checkBox_2.isChecked()
        s_3=self.checkBox_3.isChecked()
        s_4=self.checkBox_4.isChecked()
        s_5=self.checkBox_5.isChecked()
        s_6=self.checkBox_6.isChecked()
        signal_update_csr_option_value=[s_1,s_2,s_3,s_4,s_5,s_6]
        self.signal_update_csr_option.emit(signal_update_csr_option_value)
        print(signal_update_csr_option_value)
        return signal_update_csr_option_value
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = SettingDialog()
    mainWindow.show()
    sys.exit(app.exec_())