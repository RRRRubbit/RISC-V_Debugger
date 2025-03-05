# -*- coding: UTF-8 -*-
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QAction, QFileDialog
from PyQt5.QtCore import  *
import serial.tools.list_ports
import os
import argparse
import serial
from GUI.ui_MainWindow import *
#from GUI.ui_BreakPointDialog import *
from GUI.ui_PortSelect import *
from GUI.setting import *
from GUI.ui_memory_widget import *
from LOGIC.BreakPointDialog import *
from LOGIC.PortSent import *

import timeit
from PyQt5.QtSerialPort import QSerialPortInfo, QSerialPort

from LOGIC.memorywindow import Memorywidget
from LOGIC.settingdialog import SettingDialog

serial_is_open = False
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    sign_one = pyqtSignal(str)
    trigger_PortSent = pyqtSignal()
    ProgramCounter = pyqtSignal((str))
    signal_RAM_model = pyqtSignal(str)
    ScrollBar_RAM = pyqtSignal(int)

    global hexfile_dir

######initialization function##############################################################################################
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.CreateItems()
        self.CreateSignalSlot()
        self.SetListwidget()
    def CreateSignalSlot(self):
        self.actionReset_chip.triggered.connect(self.reset_chip)
        self.actionOpen_Port.triggered.connect(self.PortSent_show)
        self.actionUpdate_Register.triggered.connect(self.get_register)
        self.action_upload_framework.triggered.connect(self.PortSelect.send_from_hex_file)
        self.actionReset.triggered.connect(self.reset_program)
        self.actionLoad.triggered.connect(self.get_lst)
        self.actionList_Port.triggered.connect(self.set_Hightlight)
        self.ProgramCounter.connect(self.set_Hightlight)
        self.actionRefresh_Display.triggered.connect(self.Refresh_Display)
        self.pushButton_lookmem.clicked.connect(self.look_up_memory)
        self.pushButton_setmem.clicked.connect(self.set_memory)
        self.pushButton_setreg.clicked.connect(self.set_reg)
        self.memory_window.siganl_memory_model.connect(self.PortSelect.set_memory_model)
       # self.actionLoad.triggered.connect(self.upload)
        #self.actionRun.triggered.connect(self.PortSelect.run_code)
        self.actionRun.triggered.connect(lambda: self.PortSelect.run_code(self.setting.run_option()))
        self.actionStep_Run.triggered.connect(lambda: self.PortSelect.run_step_code(self.setting.run_option()))
        #self.actionStep_Run.triggered.connect(self.runtime_test)

        #self.actionStep_Function_Run.triggered.connect(self.PortSelect.run_step_function_code)
        self.actionUpdate_RAM.triggered.connect(self.get_RAM)
        self.actionUpdate_Port.triggered.connect(self.get_IO)
        self.actionMake_BreakPoint.triggered.connect(self.BreakPointDialog_show)
        #self.actionMake_BreakPoint.triggered.connect(self.BreakPoint.read_BreakPoints)
        self.actionClean_All_Break_Point.triggered.connect(self.clean_all_break_point)
        self.actionSet_dpc.triggered.connect(self.PortSelect.set_dpc)
        self.memory_window.comboBox_memorymodel.currentIndexChanged.connect(self.get_RAM)
        self.actionSetting.triggered.connect(self.setting_show)
        self.memory_window.verticalScrollBar_MEM.valueChanged.connect(self.on_sroll)
        self.scroll_timer.timeout.connect(self.get_ScrollBar)
        self.ScrollBar_RAM.connect(lambda scrollvalue :self.PortSelect.get_RAM(Scroll_Value=scrollvalue))
        self.pushButtonr_uart_send.clicked.connect(self.uart_send)
        self.PortSelect.signal_uart_receive.connect(self.uart_receive_update)
        self.lineEdit_uart_send.returnPressed.connect(self.pushButtonr_uart_send.click)
        #self.actionClean_All_Break_Point.triggered.connect(self.clean_all_breakpoint_text)
        # Breakpoint model signal connect
        self.PortSelect.text_receive_register.connect(self.set_register)
        self.PortSelect.text_receive_RAM.connect(self.set_RAM)
        self.PortSelect.signal_label_Port.connect(self.get_gpio)
        self.PortSelect.text_receive_IO.connect(self.set_IO)

        #self.PortSelect.text_receive_Breakpoint.connect(self.BreakPoint.set_BreakPoints_text)
        self.PortSelect.run_porcess_thread.signal_run_process.connect(self.set_processbar)
        self.PortSelect.signal_get_register.connect(self.get_register)
        self.PortSelect.signal_get_RAM.connect(self.get_RAM)
        self.PortSelect.signal_csr_info.connect(self.csr_info_update)
        self.PortSelect.signal_get_dpc.connect(self.set_hightlight)
        self.PortSelect.signal_get_dpc.connect(self.set_label_dpc)
        self.PortSelect.signal_get_IO.connect(self.get_IO)
        self.PortSelect.signal_refresh.connect(self.Refresh_Display)
        self.PortSelect.BP_signal.connect(self.make_breakpoint_text)
        #Breakpoint model signal connect
        #self.BreakPoint.BP_signal.connect(self.PortSelect.Set_Breakpoint)
        #self.BreakPoint.BP_signal.connect(self.make_breakpoint_text)
        #self.BreakPoint.BP_startread_signal.connect(self.PortSelect.Read_Breakpoint)

        #StatusBar model signal connect
        self.PortSelect.signal_status_bar.connect(self.statusBar_show)
        self.setting.checkBox_2.clicked.connect(self.memory_show)
        self.memory_window.pushButton_size_set.clicked.connect(self.get_RAM)
        self.memory_window.signal_memory_size.connect(self.PortSelect.set_memory_size)
        # self.setting.signal_update_csr_option.connect(lambda run_option :self.PortSelect.run_step_code(run_option=run_option))
        # self.setting.signal_update_csr_option.connect(lambda run_option :self.PortSelect.run_code(run_option=run_option))

    def CreateItems(self):
        self.PortSelect = PortSelectDialog()
        self.BreakPoint = BreakPointDialog()
        self.setting = SettingDialog()
        self.memory_window=Memorywidget()
        self.scroll_timer = QTimer(self)
        self.scroll_timer.setSingleShot(True)

    def PortSent_show(self):
        # 创建子窗口实例
        self.PortSelect.show()
        self.statusBar_show('PortSelect window is open')
        # dialog.stop_thread.connect(thread.stop)
        # self.thread.start()
        #PortSelect = PortSelectDialog()
        # 将信号连接到子窗口的槽函数
        # 显示子窗口
        self.PortSelect.exec_()
        # 发出信号，触发子窗口的槽函数
        #ps.closeEvent()
    def BreakPointDialog_show(self):
        #bk = BreakPointDialog()
        self.BreakPoint.show()
        self.statusBar_show('Breakpoint window is open')
        self.PortSelect.exec_()
    def memory_show(self):
        self.memory_window.show()
        self.memory_window.exec_()
    def setting_show(self):
        self.setting.show()
        self.setting.exec_()
    def statusBar_show(self,message, show_time=None):
        if show_time is None:
            self.statusbar.showMessage(message,1000)
        else:
            show_time = int(show_time)
            self.statusbar.showMessage(message, show_time)
######Breakpoint functions##############################################################################################
    def reset_chip(self):
        self.PortSelect.set_reset()
    def set_processbar(self,processbar):
        print(processbar)
        self.progressBar.setValue(processbar)
    def SetListwidget(self):
        self.listWidget_ASM.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget_ASM.customContextMenuRequested.connect(self.show_context_menu)
        # 创建断点列表
        self.breakpoints = []
        # 创建QLineEdit列表
        #self.lineEdits = [getattr(self.BreakPoint, f'lineEdit_{i:02d}') for i in range(10)]
    def look_up_memory(self):
        self.PortSelect.urc.haltreq()
        self.PortSelect.urc.debug_status_reset()
        address = int(self.lineEdit_lookmem_address.text(),16)
        value = self.PortSelect.urc.lookmem(address)
        self.label_Lookmemvalue.setText(value[-8:])
    def set_memory(self):
        self.PortSelect.urc.haltreq()
        self.PortSelect.urc.debug_status_reset()
        address = int(self.lineEdit_setmem_address.text(),16)
        value = int(self.lineEdit_setmem_value.text(),16)
        s = self.PortSelect.urc.setmem(address,value)
    def set_reg(self):
        self.PortSelect.urc.haltreq()
        self.PortSelect.urc.debug_status_reset()
        address = int(self.lineEdit_setreg_address.text(), 10)
        value = int(self.lineEdit_setreg_value.text(), 16)
        if address in range(0,32):
            s = self.PortSelect.urc.setreg(address, value)
        else:
            QMessageBox.warning(self, "Warning", "Address out range.")

    def show_context_menu(self, position):
        # 创建上下文菜单
        menu = QMenu()
        item = self.listWidget_ASM.itemAt(position)
        if item is None:
            return
        # 添加断点动作
        add_breakpoint_action = QAction('Add Breakpoint', self)
        add_breakpoint_action.triggered.connect(lambda: self.add_breakpoint(item))
        menu.addAction(add_breakpoint_action)

        # 删除断点动作
        remove_breakpoint_action = QAction('Remove Breakpoint', self)
        remove_breakpoint_action.triggered.connect(lambda: self.remove_breakpoint(item))
        menu.addAction(remove_breakpoint_action)

        # 添加设置断点动作
        enable_breakpoint_action = QAction('Enable Breakpoint', self)
        enable_breakpoint_action.triggered.connect(lambda: self.enable_breakpoint(item))
        menu.addAction(enable_breakpoint_action)

        # 禁用断点动作
        disable_breakpoint_action = QAction('Disable Breakpoint', self)
        disable_breakpoint_action.triggered.connect(lambda: self.disable_breakpoint(item))
        menu.addAction(disable_breakpoint_action)

        # 显示菜单
        menu.exec_(self.listWidget_ASM.mapToGlobal(position))

    def clean_all_breakpoint_text(self):
        listWidget_ASM=self.listWidget_ASM
        count = listWidget_ASM.count()
        line_item=[]
        for i in range(count):
            line_item.append(listWidget_ASM.item(i).text())
            if ' [Breakpoint] [Enable]' in line_item[i]:
                new_line = str(line_item[i])

                new_line=new_line.replace(' [Breakpoint] [Enable]', '')
                listWidget_ASM.item(i).setText(new_line)

            elif ' [Breakpoint] [Disable]' in line_item[i]:
                new_line = str(line_item[i])
                new_line=new_line.replace(' [Breakpoint] [Disable]', '')
                listWidget_ASM.item(i).setText(new_line)
            else:
                continue

    def make_breakpoint_text(self,BP_signal):
        #self.clean_all_breakpoint_text()
        if BP_signal == 'BPclean':
            self.breakpoints.clear()
            self.clean_all_breakpoint_text()
            print(f'Breakpoint list is {self.breakpoints}.')
        elif BP_signal == '' or BP_signal == 'ERROR':
            return
        else:
            items = self.listWidget_ASM.findItems(BP_signal+' : ', Qt.MatchFlag.MatchStartsWith)
            if items == []:
                return
            else:
                for item in items:
                    item_text = item.text()
                    if ' [Breakpoint] [Enable]' in item_text or ' [Breakpoint] [Disable]' in item_text:
                        return "ERROR"

                    else:
                        item.setText(f"{item_text} [Breakpoint] [Enable]")
                        if "Deleted" in self.breakpoints:
                            deleted_index = (self.breakpoints.index("Deleted"))
                            self.breakpoints[deleted_index] = BP_signal
                        else:
                            self.breakpoints += [BP_signal]
                    print(f'Breakpoint list is {self.breakpoints}.')




    def add_breakpoint(self, item):
        item_text = item.text()
        address_part = item_text.split(":")[0].strip()
        breakpoint_address_int = int(address_part,16)
        breakpoint_address_hex = hex(breakpoint_address_int)
        # 调用设置断点的方法，并传递 breakpoint_address_int 作为参数
        s=self.PortSelect.set_breakpoint(breakpoint_address_int)
        self.statusBar_show(f'Set breakpoint at: {item_text}')
        if s == None:
            if breakpoint_address_int not in self.breakpoints:
                if "Deleted" in self.breakpoints :
                    deleted_index=(self.breakpoints.index("Deleted"))
                    self.breakpoints[deleted_index] = breakpoint_address_int
                else:
                    self.breakpoints += [breakpoint_address_hex]
            if ' [Breakpoint]' not in item_text:
                item.setText(f"{item_text} [Breakpoint] [Enable]")
            else:
                QMessageBox.warning(self, "Warning", "There is already a Breakpoint.")
                return
            print(f'Breakpoint list is {self.breakpoints}.')
        elif s =="ERROR":
            return
        else:
            return
    def remove_breakpoint(self, item):
        item_text = item.text()
        address_part = item_text.split(":")[0].strip()
        breakpoint_address_int = int(address_part,16)
        breakpoint_address_hex = hex(breakpoint_address_int)
        if breakpoint_address_hex in self.breakpoints:
            breakpoint_index=self.breakpoints.index(breakpoint_address_hex)
            self.breakpoints[breakpoint_index]="Deleted"
            print(self.breakpoints[breakpoint_index])
            s = self.PortSelect.remove_breakpoint(breakpoint_address_int)
            print(f'Removed breakpoint at: {item_text}')
            self.statusBar_show(f'Removed breakpoint at: {item_text}')
            if s is None:
                if ' [Breakpoint] [Enable]' in item_text:
                    item.setText(item_text.replace(' [Breakpoint] [Enable]', ''))
                    # self.breakpoints.remove(item_text.replace(' [Breakpoint]', ''))
                elif ' [Breakpoint] [Disable]' in item_text:
                    item.setText(item_text.replace(' [Breakpoint] [Disable]', ''))
                else:
                    QMessageBox.warning(self, "Warning", "There is no Breakpoint.")
                print(f'Breakpoint list is {self.breakpoints}.')
        else:
            s = self.PortSelect.remove_breakpoint(breakpoint_address_int)
            return s


    def enable_breakpoint(self, item):
        item_text = item.text()
        address_part = item_text.split(":")[0].strip()
        breakpoint_address_int = int(address_part,16)
        breakpoint_address_hex = hex(breakpoint_address_int)
        if breakpoint_address_hex in self.breakpoints:
            breakpoint_index=self.breakpoints.index(breakpoint_address_hex)
            s = self.PortSelect.enable_breakpoint(breakpoint_index)
            print(f'Enable breakpoint at: {item_text}')
            self.statusBar_show(f'Enable breakpoint at: {item_text}')
            if s is None:
                if ' [Breakpoint]' not in item_text:
                    QMessageBox.warning(self, "Warning", "There is no Breakpoint.")
                elif ' [Breakpoint] [Enable]'  in item_text:
                    QMessageBox.warning(self, "Warning", "The is already Breakpoint enabled.")
                elif ' [Breakpoint] [Disable]' in item_text:
                    item.setText(item_text.replace(' [Disable]', ' [Enable]'))
                    print(f'Removed breakpoint at: {item_text}')
                else:
                    item.setText(f"{item_text} [Enable]")
                print(f'Breakpoint list is {self.breakpoints}.')
            else:
                return
        else:
            QMessageBox.warning(self, "Warning", "There is no Breakpoint.")
            return


    def disable_breakpoint(self, item):
        item_text = item.text()
        address_part = item_text.split(":")[0].strip()
        breakpoint_address_int = int(address_part,16)
        breakpoint_address_hex = hex(breakpoint_address_int)
        if breakpoint_address_hex in self.breakpoints:
            breakpoint_index=self.breakpoints.index(breakpoint_address_hex)
            s = self.PortSelect.disable_breakpoint(breakpoint_index)
            print(f'Disable breakpoint at: {item_text}')
            self.statusBar_show(f'Disable breakpoint at: {item_text}')
            if s is None:
                if ' [Breakpoint]' not in item_text:
                    QMessageBox.warning(self, "Warning", "There is no Breakpoint.")
                else:
                    item.setText(item_text.replace('[Enable]', '[Disable]'))
            else:
                return
            print(f'Breakpoint list is {self.breakpoints}.')
        else:
            QMessageBox.warning(self, "Warning", "There is no Breakpoint.")
            return

######Data geting functions##############################################################################################

    def Refresh_Display(self):
        if self.PortSelect.com.is_open == False:
            QMessageBox.warning(self, "Warning", "Please open the Serial Port.")
        else:
            self.get_RAM()
            self.get_IO()
            self.get_register()
    def on_sroll(self):
        self.scroll_timer.start(300)


    def set_label_dpc(self,pc):
        pc_str=pc
        ProgramCounter = str(hex(int(pc_str, 16))).upper()
        self.label_pc.setText('PC='+ProgramCounter[2:])
    def get_ScrollBar(self):
        s = self.memory_window.verticalScrollBar_MEM.sliderPosition() #获取Scrollbar信息
        self.ScrollBar_RAM.emit(s)
    def uart_send(self):
        messages=self.lineEdit_uart_send.text()
        self.PortSelect.com_send_data(messages)
    def uart_receive_update(self,message):
        self.textBrowser_uart_receive.insertPlainText(message)
        self.textBrowser_uart_receive.moveCursor(QTextCursor.End)
    def csr_info_update(self, csr_info):
        self.label_csr.setText(csr_info)
    def get_gpio(self,message):
        self.label_Port.setText(message)
        return
    def get_ram_model(self):
        match self.memory_window.comboBox_memorymodel.currentIndex():
            case 0:
                print("Code Memory selected")
                #self.signal_RAM_model.emit('IMEM')
                self.memory_window.verticalScrollBar_MEM.setMaximum(255)  # 0000-3fff
                return 'IMEM'
            case 1:
                print("Direct InRAM selected")
                #self.signal_RAM_model.emit('DMEM')
                self.memory_window.verticalScrollBar_MEM.setMaximum(127)  # 0000-1fff
                return 'DMEM'
        # elif sender == self.actionCode_Memory:
        #     print("Code Memory selected")
        #     self.label_RAM_model.setText('Memory model: Display program memory area')
        #     self.signal_RAM_model.emit('IMEM')
        #     self.verticalScrollBar_MEM.setMaximum(255)#0000-3fff
        #     return 'IMEM'
        # elif sender == self.actionDirect_InRAM:
        #     print("Direct InRAM selected")
        #     self.label_RAM_model.setText('Memory model: Display internal data memory area')
        #     self.signal_RAM_model.emit('DMEM')
        #     self.verticalScrollBar_MEM.setMaximum(127)#0000-1fff
        #     return 'DMEM'
        # elif sender == self.actionIndirect_InRAM:
        #     print("Indirect InRAM selected")
        #     self.label_RAM_model.setText('Memory model: Display indirect data memory area ')
        #     self.signal_RAM_model.emit('DI')
        #     self.verticalScrollBar_MEM.setMaximum(3)#0000-00ff
        #     return 'DI'
        # elif sender == self.actionExternal_RAM:
        #     print("External RAM selected")
        #     self.label_RAM_model.setText('Memory model: Display external data memory area ')
        #     self.signal_RAM_model.emit('DX')
        #     self.verticalScrollBar_MEM.setMaximum(1023)#0000-ffff
        #     return 'DX'
        #elif sender == self.get_RAM():

    def get_RAM(self):
            print("> Starting get RAM... ")
            self.statusBar_show("Getting RAM",1000)
            Scroll_Value = self.memory_window.verticalScrollBar_MEM.value()
            #print(Scroll_Value)
            ram_model = self.get_ram_model()
            s = self.PortSelect.get_RAM(Scroll_Value,ram_model)
            if s == "":
                QMessageBox.warning(self,"Warning","Could not get RAM. Please check the connection.")
                return
            elif s !="":
                if len(s) == 0:
                    QMessageBox.warning(self,"Warning","Could not get RAM. Please check the connection.")
                else:
                    #self.set_register(self.s)
                    return
            #time.sleep(0.1)
    def get_IO(self):
        self.statusBar_show("Getting IO",100)
        print("> Starting get IO... ")
        s = self.PortSelect.get_IO()
        if s == "":
            QMessageBox.warning(self, "Warning", "Could not get all ports. Please check the connection.")
            return
        elif s != "":
            if len(s) == 0:
                QMessageBox.warning(self, "Warning", "Could not get all ports. Please check the connection.")
            else:
                return

    def get_register(self):
        self.statusBar_show("Getting register",1000)
        print("> Starting get register... ")
        s = self.PortSelect.get_register()
        if s == "":
            QMessageBox.warning(self, "Warning", "Could not get all register. Please check the connection.")
            return
        elif s != "":
    #         # s = "RA RB R0 R1 R2 R3 R4 R5 R6 R7 PSW DPTR SP PC<\r><\n>FF FF FF FF FF FF FF FF FF FF ---R0--- 0000 07 0000 <\r><\n>"
             if s == None or len(s) == 0:
                 QMessageBox.warning(self, "Warning", "Could not get all register. Please check the connection.")
             else:
    #             self.get_ProgramCounter(s)
                  self.set_register(s)

    def reset_program(self):
        self.statusBar_show("resetting program", 1000)
        print("> Starting reset program... ")
        if self.PortSelect.com.is_open == True:
            s = self.PortSelect.reset_program()
            if s == "":
                QMessageBox.warning(self, "Warning", "Could not get all register. Please check the connection.")
                return
            elif s != "":
                # s = "Reset Microcontroller\r\n"
                if s == None or len(s) == 0 or s[-1] != "#":
                    QMessageBox.warning(self, "Warning", "Could not get all register. Please check the connection.")
                else:
                    self.get_ProgramCounter(s)
                    # self.set_register(self.s)
                    return
        else:
            QMessageBox.warning(self, "Warning", "Could not reset program. Please check the connection.")
    global content_exist
    def get_lst(self):
        #Clean ASM Code Zone
        self.listWidget_ASM.clear()
        self.statusBar_show("Uploading asm file")
        s, _ = QFileDialog.getOpenFileName(None, 'Open a asm file', 'D:\\', 'asm files (*.asm)')
        #s='/home/sun/下载/demo_setup_sun/main.asm'
        global asmfile_dir
        asmfile_dir = s
        if asmfile_dir == '':
            return
        else:
            with open(asmfile_dir, 'r') as f:
                lst_content = f.readlines()
                for line in lst_content:
                    self.listWidget_ASM.addItem(line)

            if asmfile_dir == None:
                print("> > > Successful: File '{}' is not found".format(asmfile_dir))
            else:
                print("Successful: File '{}' is open".format(asmfile_dir))
                self.statusBar_show("Successful: File '{}' is open".format(asmfile_dir))
            return asmfile_dir

    def set_hightlight(self, pc):
        self.statusBar_show("Hightlighting ProgramCounter")
        for index in range(self.listWidget_ASM.count()):
            item = self.listWidget_ASM.item(index)
            # 设置背景颜色
            Background = QBrush(QColor(255, 255, 255, 255))  # 黄色，带有一些透明度
            item.setBackground(Background)
        pc_str=pc
        ProgramCounter = str(hex(int(pc_str,16)))
        text_to_find = ProgramCounter[2:] + ":"
        for index in range(self.listWidget_ASM.count()):
            item = self.listWidget_ASM.item(index)
            item_text = item.text().lstrip()
            if text_to_find in item_text and item_text.startswith(text_to_find):
                self.listWidget_ASM.scrollToItem(item)
                # 设置背景颜色
                brush = QBrush(QColor(255, 255, 0, 160))  # 黄色，带有一些透明度
                item.setBackground(brush)

    ######Date processing and displaying functions##############################################################################################
    def set_RAM(self, message):
        s = message  # 去掉#
        '''
        s =(00000040: 0x00000000
00000044: 0x00000044
00000048: 0x00000048
0000004c: 0x0000004C
00000050: 0x00000050
00000054: 0x00000054
00000058: 0x00000058
0000005c: 0x0000005C
00000060: 0x00000060
00000064: 0x00000064
00000068: 0x00000068
0000006c: 0x0000006C
00000070: 0x00000070
00000074: 0x00000074
00000078: 0x00000078
0000007c: 0x0000007C
        )
        '''
        lines = s.split("\r")
        formatted_lines = []
        def hex_to_ascii(hex_str):
            bytes_array = bytes.fromhex(hex_str)
            return ''.join(chr(b) if 32 <= b <= 126 else '.' for b in bytes_array)
        for i in range(0, len(lines), 4):
            if ": " in lines[i]:
                part1 = lines[i].split(": ")[1][2:]
                part2 = lines[i + 1].split(": ")[1][2:] if i + 1 < len(lines) and ": " in lines[i + 1] else "00000000"
                part3 = lines[i + 2].split(": ")[1][2:] if i + 2 < len(lines) and ": " in lines[i + 2] else "00000000"
                part4 = lines[i + 3].split(": ")[1][2:] if i + 3 < len(lines) and ": " in lines[i + 3] else "00000000"
                address = lines[i].split(":")[0]
                hex_values = f"{part1[:2]} {part1[2:4]} {part1[4:6]} {part1[6:8]}"
                hex_values += f"{part2[:2]} {part2[2:4]} {part2[4:6]} {part2[6:8]}"
                hex_values += f"{part3[:2]} {part3[2:4]} {part3[4:6]} {part3[6:8]}"
                hex_values += f"{part4[:2]} {part4[2:4]} {part4[4:6]} {part4[6:8]}"
                ascii_values = hex_to_ascii(part1 + part2 + part3 + part4)
                formatted_lines.append(f"{address}: {hex_values[0:11]}|{hex_values[11:22]}|{hex_values[22:33]}|{hex_values[33:]} |{ascii_values}|")
        #print("\n".join(formatted_lines))
        d="\n".join(formatted_lines)
        self.memory_window.textBrowser_MEM.insertPlainText(d)
        self.memory_window.textBrowser_MEM.insertPlainText('\nMemory look up completed\n')
        return s


    def set_IO(self, message):
        #s=message.split("\r\n#dd")
        pattern= re.compile(r'D:(.+?)\r\n#')
        c=pattern.findall(message)
        i = 0
        P = ['P0 = ', 'P1 = ', 'P2 = ', 'P3 = ', 'P4 = ', 'P5 = ']
        d = ''
        e = '\r\n'
        '''
        D:80: BD
        #dd80 80
        D:90: FE 
        #dd90 90
        D:A0: 7E
        #dda0 a0
        D:B0: FD
        #ddb0 b0
        D:E8: FF
        #dde8 e8
        D:F8: 3F
        #ddf8 f8
        #di0 4f
        '''
        for line in c:
            #print(line)
            line = line.split()
            line_list = list(line)
            line_list[0]=P[i]
            i=i+1
            line_list_1_bin=bin(int(line_list[1],16))
            line_list_1_bin=line_list_1_bin.lstrip('0b')
            line_list[1]='{:0>8}'.format(line_list_1_bin)
            line = ''.join(line_list)
            d = d+line+e+e
        #print(d)
        self.label_Port.setText(d)
        return d
    def set_register(self, message):
        self.label_Reg.setText(message)
        return message

    def set_Hightlight(self, PC=None,BP=None):
        self.statusBar_show("Hightlighting ProgramCounter")
        for index in range(self.listWidget_ASM.count()):
                item = self.listWidget_ASM.item(index)
                # 设置背景颜色
                Background = QBrush(QColor(255, 255, 255, 255))  # 黄色，带有一些透明度
                item.setBackground(Background)
        ProgramCounter=PC
        text_to_find=ProgramCounter+" : "
        for index in range(self.listWidget_ASM.count()):
                item = self.listWidget_ASM.item(index)
                if text_to_find in item.text():
                    # 设置背景颜色
                    brush = QBrush(QColor(255, 255, 0, 160))  # 黄色，带有一些透明度
                    item.setBackground(brush)

    def clean_all_break_point(self):
        if self.PortSelect.com.is_open == True:
            #self.statusBar_show("Cleaning All Breakpoint")
            print("> Cleaning All Breakpoint... ")
            self.PortSelect.Com_Send_Data(message="BK ALL\r")
            s = self.PortSelect.com.read_until(expected="#".encode("utf-8")).decode("utf-8")
            self.PortSelect.textEdit_Receive.insertPlainText(s)
            self.statusBar_show(s)
            self.breakpoints.clear()
            self.clean_all_breakpoint_text()
            print(s)

        else:
            QMessageBox.warning(self, "Warning", "Please open the serial port")
            return
            #s = PortSelectDialog.(expected="#".encode("utf-8")).decode("utf-8")
            #if len(s) == 0 or s[-1] != "#":
                #raise Exception("Could not make breakpoint. Please reset and try again.")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
