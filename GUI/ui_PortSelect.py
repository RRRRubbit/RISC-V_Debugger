# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_PortSelect.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_PortSelect(object):
    def setupUi(self, Dialog_PortSelect):
        Dialog_PortSelect.setObjectName("Dialog_PortSelect")
        Dialog_PortSelect.resize(839, 401)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog_PortSelect)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 829, 294))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_ReceiveZone = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_ReceiveZone.setObjectName("label_ReceiveZone")
        self.gridLayout_2.addWidget(self.label_ReceiveZone, 0, 1, 1, 1)
        self.pushButton_Send = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_Send.setObjectName("pushButton_Send")
        self.gridLayout_2.addWidget(self.pushButton_Send, 3, 3, 1, 1)
        self.pushButto_Clear = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButto_Clear.setObjectName("pushButto_Clear")
        self.gridLayout_2.addWidget(self.pushButto_Clear, 0, 3, 1, 1)
        self.checkBox_HexSend = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.checkBox_HexSend.setObjectName("checkBox_HexSend")
        self.gridLayout_2.addWidget(self.checkBox_HexSend, 3, 2, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 3, 1, 1)
        self.checkBox_HexShow = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.checkBox_HexShow.setObjectName("checkBox_HexShow")
        self.gridLayout_2.addWidget(self.checkBox_HexShow, 0, 2, 1, 1)
        self.label_SendZone = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_SendZone.setObjectName("label_SendZone")
        self.gridLayout_2.addWidget(self.label_SendZone, 3, 1, 1, 1)
        self.textEdit_Receive = QtWidgets.QTextEdit(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_Receive.sizePolicy().hasHeightForWidth())
        self.textEdit_Receive.setSizePolicy(sizePolicy)
        self.textEdit_Receive.setMinimumSize(QtCore.QSize(200, 100))
        self.textEdit_Receive.setObjectName("textEdit_Receive")
        self.gridLayout_2.addWidget(self.textEdit_Receive, 1, 2, 1, 1)
        self.textEdit_Send = QtWidgets.QTextEdit(self.horizontalLayoutWidget_2)
        self.textEdit_Send.setMinimumSize(QtCore.QSize(200, 100))
        self.textEdit_Send.setObjectName("textEdit_Send")
        self.gridLayout_2.addWidget(self.textEdit_Send, 4, 2, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_Port = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_Port.setObjectName("label_Port")
        self.gridLayout.addWidget(self.label_Port, 0, 0, 1, 1)
        self.label_IsOpenOrNot = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_IsOpenOrNot.setText("")
        self.label_IsOpenOrNot.setObjectName("label_IsOpenOrNot")
        self.gridLayout.addWidget(self.label_IsOpenOrNot, 5, 2, 1, 1)
        self.label_Statusbar = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_Statusbar.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_Statusbar.setLineWidth(1)
        self.label_Statusbar.setText("")
        self.label_Statusbar.setObjectName("label_Statusbar")
        self.gridLayout.addWidget(self.label_Statusbar, 9, 0, 1, 1)
        self.pushButton_ClosePort = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_ClosePort.setObjectName("pushButton_ClosePort")
        self.gridLayout.addWidget(self.pushButton_ClosePort, 5, 1, 1, 1)
        self.pushButton_Refresh = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_Refresh.setObjectName("pushButton_Refresh")
        self.gridLayout.addWidget(self.pushButton_Refresh, 0, 2, 1, 1)
        self.pushButton_OpenPort = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_OpenPort.setObjectName("pushButton_OpenPort")
        self.gridLayout.addWidget(self.pushButton_OpenPort, 5, 0, 1, 1)
        self.comboBox_PortName = QtWidgets.QComboBox(self.horizontalLayoutWidget_2)
        self.comboBox_PortName.setObjectName("comboBox_PortName")
        self.gridLayout.addWidget(self.comboBox_PortName, 0, 1, 1, 1)
        self.label_BaudRate = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_BaudRate.setObjectName("label_BaudRate")
        self.gridLayout.addWidget(self.label_BaudRate, 2, 0, 1, 1)
        self.comboBox_BaudRate = QtWidgets.QComboBox(self.horizontalLayoutWidget_2)
        self.comboBox_BaudRate.setObjectName("comboBox_BaudRate")
        self.comboBox_BaudRate.addItem("")
        self.comboBox_BaudRate.addItem("")
        self.comboBox_BaudRate.addItem("")
        self.comboBox_BaudRate.addItem("")
        self.comboBox_BaudRate.addItem("")
        self.comboBox_BaudRate.addItem("")
        self.comboBox_BaudRate.addItem("")
        self.comboBox_BaudRate.addItem("")
        self.comboBox_BaudRate.addItem("")
        self.comboBox_BaudRate.addItem("")
        self.comboBox_BaudRate.addItem("")
        self.gridLayout.addWidget(self.comboBox_BaudRate, 2, 1, 1, 1)
        self.label_Time = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_Time.setMinimumSize(QtCore.QSize(150, 0))
        self.label_Time.setObjectName("label_Time")
        self.gridLayout.addWidget(self.label_Time, 6, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)

        self.retranslateUi(Dialog_PortSelect)
        QtCore.QMetaObject.connectSlotsByName(Dialog_PortSelect)

    def retranslateUi(self, Dialog_PortSelect):
        _translate = QtCore.QCoreApplication.translate
        Dialog_PortSelect.setWindowTitle(_translate("Dialog_PortSelect", "Serial Port Management"))
        self.label_ReceiveZone.setText(_translate("Dialog_PortSelect", "Receive Zone"))
        self.pushButton_Send.setText(_translate("Dialog_PortSelect", "Send"))
        self.pushButto_Clear.setText(_translate("Dialog_PortSelect", "Clear"))
        self.checkBox_HexSend.setText(_translate("Dialog_PortSelect", "Hex Send"))
        self.checkBox_HexShow.setText(_translate("Dialog_PortSelect", "Hex Show"))
        self.label_SendZone.setText(_translate("Dialog_PortSelect", "Send Zone"))
        self.label_Port.setText(_translate("Dialog_PortSelect", "Port Select"))
        self.pushButton_ClosePort.setText(_translate("Dialog_PortSelect", "Close Port"))
        self.pushButton_Refresh.setText(_translate("Dialog_PortSelect", "Refresh"))
        self.pushButton_OpenPort.setText(_translate("Dialog_PortSelect", "Open Port"))
        self.label_BaudRate.setText(_translate("Dialog_PortSelect", "Baud Rate"))
        self.comboBox_BaudRate.setItemText(0, _translate("Dialog_PortSelect", "9600"))
        self.comboBox_BaudRate.setItemText(1, _translate("Dialog_PortSelect", "14400"))
        self.comboBox_BaudRate.setItemText(2, _translate("Dialog_PortSelect", "19200"))
        self.comboBox_BaudRate.setItemText(3, _translate("Dialog_PortSelect", "38400"))
        self.comboBox_BaudRate.setItemText(4, _translate("Dialog_PortSelect", "43000"))
        self.comboBox_BaudRate.setItemText(5, _translate("Dialog_PortSelect", "57600"))
        self.comboBox_BaudRate.setItemText(6, _translate("Dialog_PortSelect", "76800"))
        self.comboBox_BaudRate.setItemText(7, _translate("Dialog_PortSelect", "115200"))
        self.comboBox_BaudRate.setItemText(8, _translate("Dialog_PortSelect", "128000"))
        self.comboBox_BaudRate.setItemText(9, _translate("Dialog_PortSelect", "256000"))
        self.comboBox_BaudRate.setItemText(10, _translate("Dialog_PortSelect", "460800"))
        self.label_Time.setText(_translate("Dialog_PortSelect", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_PortSelect = QtWidgets.QDialog()
    ui = Ui_Dialog_PortSelect()
    ui.setupUi(Dialog_PortSelect)
    Dialog_PortSelect.show()
    sys.exit(app.exec_())
