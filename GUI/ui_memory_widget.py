# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_memory_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Memory_widget(object):
    def setupUi(self, Memory_widget):
        Memory_widget.setObjectName("Memory_widget")
        Memory_widget.resize(767, 384)
        self.gridLayout_2 = QtWidgets.QGridLayout(Memory_widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_memorymodel = QtWidgets.QComboBox(Memory_widget)
        self.comboBox_memorymodel.setObjectName("comboBox_memorymodel")
        self.comboBox_memorymodel.addItem("")
        self.comboBox_memorymodel.addItem("")
        self.gridLayout.addWidget(self.comboBox_memorymodel, 0, 0, 1, 5)
        self.pushButton_size_set = QtWidgets.QPushButton(Memory_widget)
        self.pushButton_size_set.setObjectName("pushButton_size_set")
        self.gridLayout.addWidget(self.pushButton_size_set, 1, 4, 1, 1)
        self.comboBox_memorysize = QtWidgets.QComboBox(Memory_widget)
        self.comboBox_memorysize.setObjectName("comboBox_memorysize")
        self.comboBox_memorysize.addItem("")
        self.comboBox_memorysize.addItem("")
        self.gridLayout.addWidget(self.comboBox_memorysize, 1, 3, 1, 1)
        self.verticalScrollBar_MEM = QtWidgets.QScrollBar(Memory_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalScrollBar_MEM.sizePolicy().hasHeightForWidth())
        self.verticalScrollBar_MEM.setSizePolicy(sizePolicy)
        self.verticalScrollBar_MEM.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar_MEM.setObjectName("verticalScrollBar_MEM")
        self.gridLayout.addWidget(self.verticalScrollBar_MEM, 0, 5, 7, 1)
        self.lineEdit_memaddr_start = QtWidgets.QLineEdit(Memory_widget)
        self.lineEdit_memaddr_start.setObjectName("lineEdit_memaddr_start")
        self.gridLayout.addWidget(self.lineEdit_memaddr_start, 1, 2, 1, 1)
        self.textBrowser_MEM = QtWidgets.QTextBrowser(Memory_widget)
        font = QtGui.QFont()
        font.setFamily("Liberation Mono")
        font.setBold(True)
        font.setWeight(75)
        self.textBrowser_MEM.setFont(font)
        self.textBrowser_MEM.setObjectName("textBrowser_MEM")
        self.gridLayout.addWidget(self.textBrowser_MEM, 2, 0, 5, 5)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Memory_widget)
        QtCore.QMetaObject.connectSlotsByName(Memory_widget)

    def retranslateUi(self, Memory_widget):
        _translate = QtCore.QCoreApplication.translate
        Memory_widget.setWindowTitle(_translate("Memory_widget", "Form"))
        self.comboBox_memorymodel.setItemText(0, _translate("Memory_widget", "IMEM"))
        self.comboBox_memorymodel.setItemText(1, _translate("Memory_widget", "DMEM"))
        self.pushButton_size_set.setText(_translate("Memory_widget", "OK"))
        self.comboBox_memorysize.setItemText(0, _translate("Memory_widget", "64byte"))
        self.comboBox_memorysize.setItemText(1, _translate("Memory_widget", "256byte"))
        self.lineEdit_memaddr_start.setPlaceholderText(_translate("Memory_widget", "Start address(hex)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Memory_widget = QtWidgets.QWidget()
    ui = Ui_Memory_widget()
    ui.setupUi(Memory_widget)
    Memory_widget.show()
    sys.exit(app.exec_())
