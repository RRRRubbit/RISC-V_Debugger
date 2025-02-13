from PyQt5.QtWidgets import QAction, QFileDialog
from PyQt5.QtCore import *
from GUI.ui_BreakPointDialog import *
from GUI.ui_MainWindow import *
from LOGIC.PortSent import *

class BreakPointDialog(QtWidgets.QDialog, Ui_Dialog):
    BP_signal=pyqtSignal(str)
    BP_startread_signal = pyqtSignal(str)
    def __init__(self, parent=None):
        super(BreakPointDialog, self).__init__(parent)
        self.setupUi(self)
        # 设置实例
        self.CreateItems()
        # 设置信号与槽
        self.CreateSignalSlot()
       # self.cleanAllBreakPoints()

    def CreateItems(self):
        return

    def CreateSignalSlot(self):
        # 连接语句
        self.buttonBox.accepted.connect(self.set_BreakPoints)
        # self.lineEdit_00.setInputMask('HHHH;_'),self.lineEdit_01.setInputMask('HHHH;_'),self.lineEdit_02.setInputMask('HHHH;_')

    # 槽函数
    def cleanAllBreakPoints(self):
        self.BP_signal.emit('BPclean')
        return
    def set_BreakPoints(self):
        self.cleanAllBreakPoints()

        BP = {}
        BP[0]=self.lineEdit_00.text()
        BP[1]=self.lineEdit_01.text()
        BP[2]=self.lineEdit_02.text()
        BP[3]=self.lineEdit_03.text()
        BP[4]=self.lineEdit_04.text()
        BP[5]=self.lineEdit_05.text()
        BP[6]=self.lineEdit_06.text()
        BP[7]=self.lineEdit_07.text()
        BP[8]=self.lineEdit_08.text()
        BP[9]=self.lineEdit_09.text()

            #BP_address=BP_0
        for i in range(0,9):
            self.BP_signal.emit(BP[i])
    def read_BreakPoints(self):
        signal_s='start read Breakpoint'
        self.BP_startread_signal.emit(signal_s)


        return
    def set_BreakPoints_text(self, current_text):
        if current_text == '':
            #QMessageBox.critical(self, 'Warning', '', )
            return None
        elif current_text == 'BL\r\n#':#if no Breakpoint set
            # Assuming self.lineEdit_00 to self.lineEdit_09 are defined somewhere in your class
            self.lineEdits = [
                self.lineEdit_00, self.lineEdit_01, self.lineEdit_02, self.lineEdit_03,
                self.lineEdit_04, self.lineEdit_05, self.lineEdit_06, self.lineEdit_07,
                self.lineEdit_08, self.lineEdit_09
            ]

            for line_edit in self.lineEdits:
                line_edit.clear()

        else:
            self.lineEdits = [
                self.lineEdit_00, self.lineEdit_01, self.lineEdit_02, self.lineEdit_03,
                self.lineEdit_04, self.lineEdit_05, self.lineEdit_06, self.lineEdit_07,
                self.lineEdit_08, self.lineEdit_09
            ]
            for line_edit in self.lineEdits:
                line_edit.clear()
            lines = current_text.strip().split('\r\n')
            if 'ERROR' in lines[1]:#判断是否有ERROR
                QMessageBox.critical(self,'Error Address set','Error')
            else:
                lines = [line for line in lines if line and not line.startswith('#')]
                current_text = [line.split(':')[1] for line in lines if ':' in line]
                current_index =  [line.split(':')[0] for line in lines if ':' in line]
                for i in range(len(current_text)):
                    current_Address = current_text[i]
                    if current_Address:
                        current_text[i] = current_Address[-4:]
                #breakpoint_dict=dict(zip(current_index,current_text))
                breakpoint_dict = {'current_index': current_index, 'current_text' : current_text}

            self.lineEdits = [
                self.lineEdit_00, self.lineEdit_01, self.lineEdit_02, self.lineEdit_03,
                self.lineEdit_04, self.lineEdit_05, self.lineEdit_06, self.lineEdit_07,
                self.lineEdit_08, self.lineEdit_09
            ]

            def update_lineEdits(lineEdits, breakpoint_dict):
                #self.lineEdits.clear()
                for i, index in enumerate(breakpoint_dict['current_index']):
                    # Convert index to integer and subtract 1 to match zero-based indexing of list
                    edit_index = int(index)
                    if 0 <= edit_index < len(lineEdits):
                        lineEdits[edit_index].setText(breakpoint_dict['current_text'][i])
            update_lineEdits(self.lineEdits, breakpoint_dict)
                # for i, text_widget in enumerate([self.lineEdit_00, self.lineEdit_01, self.lineEdit_02, self.lineEdit_03,
                #                                  self.lineEdit_04, self.lineEdit_05, self.lineEdit_06, self.lineEdit_07,
                #                                  self.lineEdit_08, self.lineEdit_09], start=0):
                #     for j in enumerate(breakpoint_dict)
                #     if i < len(current_text) and current_text[i]:  # 检查索引是否有效且值非空
                #         if i == breakpoint_dict[current_index[i]]
                #         text_widget.setText(current_text[i])
                        # 否则不执行赋值操作，text_widget将保持其当前值或默认值

            # self.lineEdit_00.text = current_text[0]
            # self.lineEdit_01.text = current_text[1]
            # self.lineEdit_02.text = current_text[2]
            # self.lineEdit_03.text = current_text[3]
            # self.lineEdit_04.text = current_text[4]
            # self.lineEdit_05.text = current_text[5]
            # self.lineEdit_06.text = current_text[6]
            # self.lineEdit_07.text = current_text[7]
            # self.lineEdit_08.text = current_text[8]
            # self.lineEdit_09.text = current_text[9]


#
#
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = BreakPointDialog()
    mainWindow.show()
    sys.exit(app.exec_())


