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
        Dialog_PortSelect.resize(627, 562)
        Dialog_PortSelect.setSizeGripEnabled(True)
        self.gridLayout_3 = QtWidgets.QGridLayout(Dialog_PortSelect)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_ReceiveZone = QtWidgets.QLabel(Dialog_PortSelect)
        self.label_ReceiveZone.setObjectName("label_ReceiveZone")
        self.gridLayout_2.addWidget(self.label_ReceiveZone, 1, 1, 1, 1)
        self.textEdit_Send = QtWidgets.QTextEdit(Dialog_PortSelect)
        self.textEdit_Send.setMinimumSize(QtCore.QSize(200, 100))
        self.textEdit_Send.setObjectName("textEdit_Send")
        self.gridLayout_2.addWidget(self.textEdit_Send, 4, 1, 1, 3)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_Refresh = QtWidgets.QPushButton(Dialog_PortSelect)
        self.pushButton_Refresh.setObjectName("pushButton_Refresh")
        self.gridLayout.addWidget(self.pushButton_Refresh, 0, 2, 1, 1)
        self.label_IsOpenOrNot = QtWidgets.QLabel(Dialog_PortSelect)
        self.label_IsOpenOrNot.setText("")
        self.label_IsOpenOrNot.setObjectName("label_IsOpenOrNot")
        self.gridLayout.addWidget(self.label_IsOpenOrNot, 4, 2, 1, 1)
        self.label_BaudRate = QtWidgets.QLabel(Dialog_PortSelect)
        self.label_BaudRate.setObjectName("label_BaudRate")
        self.gridLayout.addWidget(self.label_BaudRate, 2, 0, 1, 1)
        self.label_Time = QtWidgets.QLabel(Dialog_PortSelect)
        self.label_Time.setMinimumSize(QtCore.QSize(150, 0))
        self.label_Time.setObjectName("label_Time")
        self.gridLayout.addWidget(self.label_Time, 2, 2, 1, 1)
        self.label_Port = QtWidgets.QLabel(Dialog_PortSelect)
        self.label_Port.setObjectName("label_Port")
        self.gridLayout.addWidget(self.label_Port, 0, 0, 1, 1)
        self.comboBox_PortName = QtWidgets.QComboBox(Dialog_PortSelect)
        self.comboBox_PortName.setObjectName("comboBox_PortName")
        self.gridLayout.addWidget(self.comboBox_PortName, 0, 1, 1, 1)
        self.pushButton_ClosePort = QtWidgets.QPushButton(Dialog_PortSelect)
        self.pushButton_ClosePort.setObjectName("pushButton_ClosePort")
        self.gridLayout.addWidget(self.pushButton_ClosePort, 4, 1, 1, 1)
        self.comboBox_BaudRate = QtWidgets.QComboBox(Dialog_PortSelect)
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
        self.pushButton_OpenPort = QtWidgets.QPushButton(Dialog_PortSelect)
        self.pushButton_OpenPort.setObjectName("pushButton_OpenPort")
        self.gridLayout.addWidget(self.pushButton_OpenPort, 4, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 3)
        self.checkBox_HexShow = QtWidgets.QCheckBox(Dialog_PortSelect)
        self.checkBox_HexShow.setObjectName("checkBox_HexShow")
        self.gridLayout_2.addWidget(self.checkBox_HexShow, 1, 2, 1, 1)
        self.pushButto_Clear = QtWidgets.QPushButton(Dialog_PortSelect)
        self.pushButto_Clear.setObjectName("pushButto_Clear")
        self.gridLayout_2.addWidget(self.pushButto_Clear, 1, 3, 1, 1)
        self.pushButton_Send = QtWidgets.QPushButton(Dialog_PortSelect)
        self.pushButton_Send.setCheckable(False)
        self.pushButton_Send.setObjectName("pushButton_Send")
        self.gridLayout_2.addWidget(self.pushButton_Send, 3, 3, 1, 1)
        self.checkBox_HexSend = QtWidgets.QCheckBox(Dialog_PortSelect)
        self.checkBox_HexSend.setObjectName("checkBox_HexSend")
        self.gridLayout_2.addWidget(self.checkBox_HexSend, 3, 2, 1, 1)
        self.label_SendZone = QtWidgets.QLabel(Dialog_PortSelect)
        self.label_SendZone.setObjectName("label_SendZone")
        self.gridLayout_2.addWidget(self.label_SendZone, 3, 1, 1, 1)
        self.textBrowser_Receive = QtWidgets.QTextBrowser(Dialog_PortSelect)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser_Receive.sizePolicy().hasHeightForWidth())
        self.textBrowser_Receive.setSizePolicy(sizePolicy)
        self.textBrowser_Receive.setMinimumSize(QtCore.QSize(200, 100))
        self.textBrowser_Receive.setObjectName("textBrowser_Receive")
        self.gridLayout_2.addWidget(self.textBrowser_Receive, 2, 1, 1, 3)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Dialog_PortSelect)
        QtCore.QMetaObject.connectSlotsByName(Dialog_PortSelect)

    def retranslateUi(self, Dialog_PortSelect):
        _translate = QtCore.QCoreApplication.translate
        Dialog_PortSelect.setWindowTitle(_translate("Dialog_PortSelect", "Serial Port Management"))
        self.label_ReceiveZone.setText(_translate("Dialog_PortSelect", "Receive Zone"))
        self.pushButton_Refresh.setText(_translate("Dialog_PortSelect", "Refresh"))
        self.label_BaudRate.setText(_translate("Dialog_PortSelect", "Baud Rate"))
        self.label_Time.setText(_translate("Dialog_PortSelect", "TextLabel"))
        self.label_Port.setText(_translate("Dialog_PortSelect", "Port Select"))
        self.pushButton_ClosePort.setText(_translate("Dialog_PortSelect", "Close Port"))
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
        self.pushButton_OpenPort.setText(_translate("Dialog_PortSelect", "Open Port"))
        self.checkBox_HexShow.setText(_translate("Dialog_PortSelect", "Hex Show"))
        self.pushButto_Clear.setText(_translate("Dialog_PortSelect", "Clear"))
        self.pushButton_Send.setText(_translate("Dialog_PortSelect", "Send"))
        self.pushButton_Send.setShortcut(_translate("Dialog_PortSelect", "Return"))
        self.checkBox_HexSend.setText(_translate("Dialog_PortSelect", "Hex Send"))
        self.label_SendZone.setText(_translate("Dialog_PortSelect", "Send Zone"))
