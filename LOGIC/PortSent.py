import re
import sys
from PyQt5.QtGui import QRegularExpressionValidator, QTextCursor
from PyQt5.QtCore import QRegularExpression  # PyQt5
import binascii
import threading
import subprocess
import time
import serial
import serial.tools.list_ports
from PyQt5.QtCore import QTimer, QUrl, pyqtSignal, QObject
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QPushButton, QMainWindow, QProgressDialog
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow
#from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QThread
#from Gui.ui_BreakPointDialog import *
#from Gui.ui_MainWindow import *
from GUI.ui_PortSelect import *
#from Logic.mainwindow import *
from LOGIC.pyurj import *
class PortSelectDialog(QtWidgets.QDialog, Ui_Dialog_PortSelect):
    text_receive_register=pyqtSignal(str)
    text_receive_RAM = pyqtSignal(str)
    text_receive_IO =pyqtSignal(str)
    text_receive_Breakpoint =pyqtSignal(str)
    signal_get_register=pyqtSignal(str)
    signal_get_RAM=pyqtSignal(str)
    signal_get_IO=pyqtSignal(str)
    signal_get_dpc = pyqtSignal(str)
    signal_csr_info = pyqtSignal(str)
    signal_status_bar = pyqtSignal(str)
    signal_refresh = pyqtSignal(str)
    BP_signal = pyqtSignal(str)
    signal_com_sending = pyqtSignal(bool)
    signal_label_Port = pyqtSignal(str)
    signal_run_process = pyqtSignal(int)
    signal_uart_receive = pyqtSignal(str)
    signal_memory_size = pyqtSignal(int)
    def __init__(self, parent=None):
        super(PortSelectDialog, self).__init__(parent)
        self.receive_thread = None
        self.timer = None
        self.com = None
        self.urc=None
        self.setupUi(self)
        self.run_porcess_thread=None
        self.signal_com_sending = False
        self.memory_size = 64
        self.memory_model = 'IMEM'
        # 设置实例
        self.create_items()
        # 设置信号与槽
        self.create_signal_slot()
    def open_serial_port(self):
        global serial_is_open
        serial_is_open = True
    # 设置实例
    def create_items(self):
        #Qt 串口类
        #self.com = QSerialPort()
        #serial串口类
        self.com = serial.Serial()
        self.urc = UrjtagTermin()
        # Qt 定时器类
        # 创建串口管理器实例
        #self.serial_manager = self.SerialManager()
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.show_time)  # 计时结束调用operate()方法
        self.timer_urc = QTimer(self)  # 初始化一个定时器
        self.timer_urc.timeout.connect(self.urc_connection_detect)  # 计时结束调用operate()方法
        self.timer_urc.start(10000)
        self.timer.start(100)  # 设置计时间隔 100ms 并启动
        self.receive_thread = ComReceiveThread(self.com, self.textBrowser_Receive, self.com_close_button_clicked, self.checkBox_HexShow, self.signal_status_bar,self.signal_uart_receive)
        self.receive_thread.start()
        self.run_porcess_thread=Processbar(self.signal_run_process)
    # 设置信号与槽
    def create_signal_slot(self):
        self.pushButton_OpenPort.clicked.connect(self.com_open_button_clicked)
        self.pushButton_ClosePort.clicked.connect(self.com_close_button_clicked)
        self.pushButton_Send.clicked.connect(self.send_button_clicked)
        self.pushButton_Refresh.clicked.connect(self.com_refresh_button_clicked)
        self.timer.timeout.connect(self.receive_thread.run)  # 接收数据
        self.checkBox_HexShow.stateChanged.connect(self.hex_showing_clicked)
        self.checkBox_HexSend.stateChanged.connect(self.hex_sending_clicked)
        self.pushButto_Clear.clicked.connect(self.clean_receive_zone)
        ####测试区域
        #self.checkBox_AutoSend.stateChanged.connect(self.progress)
        ####测试区域
    def urc_connection_detect(self):
        if self.urc.connection_detect() is True:
            return
        else:
            QMessageBox.warning(self, "Warning", "Can not detect JTAG device please check and try again")
            return
    # 显示时间
    def show_time(self):
        self.label_Time.setText(time.strftime("%B %d, %H:%M:%S", time.localtime()))
#####Upload function###################################################################################################
    def send_from_hex_file(self):
        if not self.com.is_open:
            QMessageBox.warning(self, "Warning", "Please Open Serial Port")
            return
        else:
            #设置进度条
            self.progress_dialog = QProgressDialog('Uploading Hex File...', 'Cancel', 0, 100, self)
            self.progress_dialog.setAutoClose(True)
            self.progress_dialog.setAutoReset(True)
            self.progress_dialog.canceled.connect(self.cancel_upload)
            self.upload_thread = None
            #初始化进度条信息
            self.progress_dialog.setValue(0)
            self.progress_dialog.show()
            #打开串口
            self.file_path, _ = QFileDialog.getOpenFileName(self, 'Open bin file', '', 'bin Files (*.bin)')
            #self.file_path = '/home/sun/下载/demo_setup_sun/neorv32_exe.bin'
            if not self.file_path:
                QMessageBox.warning(self, "Warning", "No file selected")
                return
            #创建线程实例
            self.upload_thread=UploadThread(self.com, self.file_path, self.signal_status_bar)
            self.upload_thread.progress.connect(self.update_progress)
            self.upload_thread.display.connect(self.receive_thread.receive_zone_update)
            self.upload_thread.finished.connect(self.upload_finished)
            self.upload_thread.start()
    def update_progress(self, value):
        if value == -1:
            QMessageBox.critical(self, "Error", "An error occurred during upload")
            self.progress_dialog.cancel()
        else:
            self.progress_dialog.setValue(value)

    def upload_finished(self):
        self.progress_dialog.setValue(100)
        QMessageBox.information(self, "Success", "Upload finished successfully")

    def cancel_upload(self):
        if self.upload_thread != None:
            if self.upload_thread.isRunning():
                self.upload_thread.terminate()
        else:
            return
        self.progress_dialog.reset()
        QMessageBox.warning(self, "Canceled", "Upload canceled")

#######NEW CODE###################################################################

    def set_dpc(self,address):
            """弹出输入对话框，限制输入为 0 开头的 16 进制数"""
            input_dialog = QInputDialog(self)
            input_dialog.setInputMode(QInputDialog.TextInput)
            input_dialog.setWindowTitle("输入 16 进制数")
            input_dialog.setLabelText("please input hex nubmer（like 0x1A3F）:")

            # 创建正则表达式，限制格式为 0x 开头的 16 进制数（可选大小写）
            hex_regex = QRegularExpression(r"^0[xX][0-9a-fA-F]+$")
            validator = QRegularExpressionValidator(hex_regex, self)
            # 获取输入框并设置校验器
            line_edit = input_dialog.findChild(QLineEdit)
            if line_edit:
                line_edit.setValidator(validator)
            # 显示对话框
            if input_dialog.exec_() == QInputDialog.Accepted:
                text = input_dialog.textValue()
                decimal_value = int(text, 16)
                # 将十进制数转换回 16 进制字符串（带 "0x" 前缀）
                if text:
                    self.urc.dpc_set(decimal_value)
                    self.signal_get_dpc.emit(self.urc.dpc_read())
    def get_register(self):
        return self.urc.lookreg()
    def set_reset(self):
        self.urc.reset()
    def set_breakpoint(self,address):
        self.urc.haltreq()
        #self.urc.dcsr_detect()
        self.urc.dpc_read()
        c=self.urc.trigger_model_csr_read()
        self.signal_get_dpc.emit(c[5][4])
        self.signal_csr_info.emit(c[-1])
        self.urc.trigger_set(0x68001044, 'tdata1')
        self.urc.trigger_set(address, 'tdata2')
    def remove_breakpoint(self,address):
        self.urc.haltreq()
        self.urc.trigger_set(0x60000040, 'tdata1')
        self.urc.trigger_set(address, 'tdata2')
        c = self.urc.trigger_model_csr_read()
        self.signal_get_dpc.emit(c[5][4])
        self.signal_csr_info.emit(c[-1])
        #self.urc.dpc_set(int(self.urc.dpc_read(), 16) + 4)
        self.urc.dpc_read()
        return
    def enable_breakpoint(self,address):
        self.urc.haltreq()
        self.urc.trigger_set(0x68001044, 'tdata1')
        self.urc.trigger_set(address, 'tdata2')
        c = self.urc.trigger_model_csr_read()
        self.signal_get_dpc.emit(c[5][4])
        self.signal_csr_info.emit(c[-1])
        #self.urc.dpc_set(int(self.urc.dpc_read(), 16) + 4)
        self.urc.dpc_read()
        return
    def disable_breakpoint(self,address):
        self.urc.haltreq()
        #self.urc.dcsr_detect()
        self.urc.dpc_read()
        self.urc.trigger_set(0x68001040, 'tdata1')
        self.urc.trigger_set(address, 'tdata2')
        c = self.urc.trigger_model_csr_read()
        self.signal_get_dpc.emit(c[5][4])
        self.signal_csr_info.emit(c[-1])
        #self.urc.dpc_set(int(self.urc.dpc_read(), 16) + 4)
        self.urc.dpc_read()
        return
    def run_code(self,run_option=None):
        self.run_porcess_thread.start()
        self.urc.haltreq()
        #self.urc.dcsr_set(None)
        step_count = 0
        if run_option is None:
            run_option = [False, False, False, True, False, False]
        else:
            run_option = run_option
        total_steps = sum(run_option)  # 计算总步骤数
        def update_progress():
            nonlocal step_count
            step_count += 1
            progress_value = int((step_count / total_steps) * 100)
            self.run_porcess_thread.signal_run_process.emit(progress_value)
        a = b = c = ''
        if run_option[0]:self.signal_get_register.emit('Run code then get Reg'),update_progress()
        if run_option[1]:self.signal_get_RAM.emit('Run code then get RAM'),update_progress()
        if run_option[2]:a = self.urc.machine_csr_read()[-1];update_progress()
        if run_option[3]:b = self.urc.trigger_model_csr_read()[-1];update_progress()
        if run_option[4]:c = self.urc.counter_time_csr_read()[-1];update_progress()
        if run_option[5]:self.signal_label_Port.emit('P0 = ' + self.urc.gpio_read()),update_progress()
        messages=a+b+c

        dpc=self.urc.dpc_read()
        dcsr_str=self.urc.dcsr_read()[0][-1]
        if dcsr_str=='40000514':
            self.urc.dcsr_detect(dcsr_str)
            self.urc.dcsr_set(None)
        elif dcsr_str=='40000490' or dcsr_str=='40000494':
            self.signal_get_dpc.emit(dpc)
            self.urc.dcsr_detect(dcsr_str)
            trigger_data1_str = self.urc.trigger_tdata1_detect()[0][-1]
            print('trigger_data1=', trigger_data1_str, '\n')
            if trigger_data1_str == '68001044':
                dpc = self.urc.dpc_read()
                # 弹出对话框
                reply = QMessageBox.question(
                    self, "Breakpoint hit",
                    f"CPU stop at  {dpc}, if clean the breakpoint？",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.urc.trigger_set(0x60000040, 'tdata1')
                    self.signal_breakpoint_address.emit()
                    print('trigger data1 is clean to 0x60000040\n')
                    QMessageBox.information(self, "clean successful", "breakpoint clean successful！")
        self.signal_get_dpc.emit(dpc)
        self.signal_csr_info.emit(messages)
        self.urc.haltresumereq()
        return
    def run_step_code(self,run_option=None):
        self.urc.haltreq()
        #self.urc.dcsr_detect()
        self.urc.dcsr_set('STEP')
        step_count = 0  # 当前已执行的步骤
        if run_option is None:
            run_option = [False, False, False, False, False, False]
        else:
            run_option = run_option
        total_steps = sum(run_option)  # 计算总步骤数
        def update_progress():
            nonlocal step_count
            step_count += 1
            progress_value = int((step_count / total_steps) * 100)
            self.run_porcess_thread.signal_run_process.emit(progress_value)
        a = b = c = ''
        if run_option[0]: self.signal_get_register.emit('Run code then get Reg'), update_progress()
        if run_option[1]: self.signal_get_RAM.emit('Run code then get RAM'), update_progress()
        if run_option[2]: a = self.urc.machine_csr_read()[-1];update_progress()
        if run_option[3]: b = self.urc.trigger_model_csr_read()[-1];update_progress()
        if run_option[4]: c = self.urc.counter_time_csr_read()[-1];update_progress()
        if run_option[5]: self.signal_label_Port.emit('P0 = ' + self.urc.gpio_read()), update_progress()
        messages=a+b+c
        dpc=self.urc.dpc_read()
        dcsr_str=self.urc.dcsr_read()[0][-1]
        if dcsr_str=='40000514':
            self.urc.dcsr_detect(dcsr_str)
            #self.urc.dcsr_set(None)
        elif dcsr_str=='40000490' or dcsr_str=='40000494':
            self.signal_get_dpc.emit(dpc)
            self.urc.dcsr_detect(dcsr_str)
            trigger_data1_str = self.urc.trigger_tdata1_detect()[0][-1]
            print('trigger_data1=', trigger_data1_str, '\n')
            if trigger_data1_str == '68001044':
                dpc = self.urc.dpc_read()
                # 弹出对话框
                reply = QMessageBox.question(
                    self, "Breakpoint hit",
                    f"CPU stop at  {dpc}, if clean the breakpoint？",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.urc.trigger_set(0x60000040, 'tdata1')
                    print('trigger data1 is clean to 0x60000040\n')
                    QMessageBox.information(self, "clean successful", "breakpoint clean successful！")
        self.signal_get_dpc.emit(dpc)
        self.signal_csr_info.emit(messages)
        self.urc.haltresumereq()
        return

    def set_memory_model(self,Memory_model=None):
        if Memory_model is None:
            return
        else:
            self.memory_model = Memory_model
    def set_memory_size(self,Memory_size=None):
        if Memory_size is None:
            return
        else:
            self.memory_size = Memory_size

    def get_mem(self, Scroll_Value=None, Model=None,Memory_size=None):
        if Memory_size is None:
            Memory_size = self.memory_size
        RAM_model = self.memory_model
        if self.urc.debug_status_detect == False:
            QMessageBox.warning(self, "Warning", "Please Open Serial Port")
            return
        else:
            if Scroll_Value == None:
                self.signal_status_bar.emit("Getting RAM")
                match RAM_model:
                    case 'IMEM':
                        s=self.urc.lookmem_range(0x00000000,0x00000000+Memory_size)
                    case 'DMEM':
                        s=self.urc.lookmem_range(0x80000000, 0x80000000+Memory_size)
            else:
                match RAM_model:
                    case 'IMEM':
                        start = 0x00000000 + Scroll_Value * 64  # 添加偏移
                        end = 0x00000000+Memory_size + Scroll_Value * 64
                    case 'DMEM':
                        start = 0x80000000 + Scroll_Value * 64  # 添加偏移
                        end = 0x80000000+Memory_size + Scroll_Value * 64
                start_str = hex(start)[2:]  # 去掉0x前缀
                end_str = hex(end)[2:]
                start_str = start_str.zfill(4)
                end_str = end_str.zfill(4)
                match RAM_model:
                    case 'IMEM':
                        self.urc.debug_status_reset()
                        s=self.urc.lookmem_range(start,end)
                    case 'DMEM':
                        self.urc.debug_status_reset()
                        s = self.urc.lookmem_range(start, end)
            if len(s) == 0:
                raise Exception("Could not display program memory area. Please reset and try again.")
            else:
                self.text_receive_RAM.emit(s)
            self.memory_size = Memory_size
        return s
    def get_IO(self):
        self.signal_label_Port.emit('GPIO OUT = ' + self.urc.gpio_read())
        return self.urc.gpio_read()
###################################################################################
    ####从这里开始补充测试
    # 串口发送数据
    def com_send_data(self, message=None):
        if self.com.is_open:
            tx_data = self.textEdit_Send.toPlainText()
            if len(tx_data) == 0 and message is None:
                return
            elif len(tx_data) == 0 and message is not None:
                #message=message+"\r"
                self.signal_status_bar.emit("Sending Data")
                self.com.write(message.encode('UTF-8'))
                self.com.write('\r'.encode('UTF-8'))
                return
            elif self.checkBox_HexSend.isChecked() == False:
                self.signal_status_bar.emit("Sending Data")
                self.com.write(tx_data.encode('UTF-8'))
                self.com.write('\r'.encode('UTF-8'))
            else:
                data = tx_data.replace(' ', '')
                # 如果16进制不是偶数个字符, 去掉最后一个, [ ]左闭右开
                if len(data) % 2 == 1:
                    data = data[0:len(data) - 1]
                # 如果遇到非16进制字符
                if data.isalnum() is False:
                    QMessageBox.critical(self, 'Error', 'Contains non-hexadecimal numbers')
                try:
                    hexData = binascii.a2b_hex(data)
                except:
                    QMessageBox.critical(self, 'Error', 'Conversion encoding error')
                    return
                # 发送16进制数据, 发送格式如 ‘31 32 33 41 42 43’, 代表'123ABC'
                try:
                    self.com.write(hexData)
                except:
                    QMessageBox.critical(self, 'Abnormal', 'Hexadecimal sending error')
                    return
#串口接受
    def com_receive_data(self):
        def display_data(self, rxData):
            self.textBrowser_Receive.insertPlainText(rxData)
    # 串口刷新
    def com_refresh_button_clicked(self):
        self.comboBox_PortName.clear()
        com_list = list(serial.tools.list_ports.comports())
        ports = ""
        for info in com_list:
            #ports.join(info.device)
            #com.setPort(info)
            #if self.SerialManager.open():
            self.comboBox_PortName.addItem(info.device)
        #com.close()
    # 16进制显示按下
    def hex_showing_clicked(self):
        if self.checkBox_HexShow.isChecked() == True:
            # 接收区换行
            self.textBrowser_Receive.insertPlainText('\n')

    # 16进制发送按下
    def hex_sending_clicked(self):
        if self.checkBox_HexSend.isChecked() == True:
            pass

    # 发送按钮按下
    def send_button_clicked(self):
        self.com_send_data()
        #SendThread_thread=SendThread()
        #SendThread_thread.start()

    # 串口刷新按钮按下
    def com_open_button_clicked(self):
        #open serial signol send then serial_is_open==True
        self.open_serial_port()
        #### com Open Code here ####
        # comName = '/dev/ttyACM0'
        # comBaud = 19200
        comName = self.comboBox_PortName.currentText()
        comBaud = int(self.comboBox_BaudRate.currentText())
        self.com.port=comName
        self.com.baudrate=comBaud

        try:
            self.com.open()
            # if com.is_open == True:
            #     #QMessageBox.critical(self, 'Fatal error', 'The serial port failed to be opened')
            #     return
        except:
            QMessageBox.critical(self, 'Fatal error', 'The serial port failed to be opened')
            return
        print("> Connecting to Labbord...")
        self.signal_status_bar.emit("> Connecting to Labbord...")
        self.pushButton_ClosePort.setEnabled(True)
        self.pushButton_OpenPort.setEnabled(False)
        self.pushButton_Refresh.setEnabled(False)
        self.comboBox_PortName.setEnabled(False)
        self.comboBox_BaudRate.setEnabled(False)
        self.label_IsOpenOrNot.setText('  Opened')
        #self.com.setBaudRate(comBaud)

    def com_close_button_clicked(self):
        if self.com.is_open:
            # 先暂停串口读取
            #self.com.blockSignals(True)
            # 关闭串口
            self.com.close()
            print("Serial port closed")
            self.signal_status_bar.emit("Serial port closed")
            # 恢复串口读取
            #self.com.blockSignals(False)
        else:
            print("Serial port is not open")

        self.pushButton_ClosePort.setEnabled(False)
        self.pushButton_OpenPort.setEnabled(True)
        self.pushButton_Refresh.setEnabled(True)
        self.comboBox_PortName.setEnabled(True)
        self.comboBox_BaudRate.setEnabled(True)
        self.label_IsOpenOrNot.setText('  Closed')

    def clean_receive_zone(self):
        self.textEdit_Receive.clear()

    def closeEvent(self, event):
        # Check if the serial port is open
        if self.com and self.com.isOpen():
            # Serial port is open, hide the window
            event.ignore()  # Ignore the close event
            QMessageBox.critical(self, 'Warning', 'The serial port is still open', )
            self.hide()  # Hide the window
        else:
            # Serial port is not open, close the window
            self.close()  # Accept the close event

class Processbar(QThread):
    signal_run_process = pyqtSignal(int)
    def __init__(self, signal_run_process):
        super().__init__()
        self.signal_run_process = signal_run_process
    def run(self):
        # for i in range(100):
        #     self.signal_run_process.emit(i)
        #     print(f'process is {i}')
        return
class UploadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(int)
    display = pyqtSignal(str)

    def __init__(self, com, file_path, signal_status_bar):
        super().__init__()
        self.com = com
        self.file_path = file_path
        #self.file_path='/home/sun/下载/demo_setup_sun/neorv32_exe.bin'
        self.signal_status_bar = signal_status_bar

    def run(self):
        try:
            with open(self.file_path, 'rb') as file:
                lines = file.read()
                self.com.write(('u').encode("utf-8"))
                time.sleep(0.1)
                self.com.write(lines)
                time.sleep(0.1)
                self.com.write(('e').encode("utf-8"))
                # for i, line in enumerate(lines):
                #     # if self.com.in_waiting:  # 串口缓冲区有数据
                #     print(line)
                #     self.com.write(line)
                #     # time.sleep(0.01)  # Simulate a delay in sending data
                #     #progress_percent = int((i + 1) / total_lines * 100)
                #     #progress_percent = 100
                # #     print(progress_percent)
                # # #     # print(line)
                # #     self.progress.emit(progress_percent)
                # #     if progress_percent == 100:
                self.finished.emit(1)
        except Exception as e:
            print(f"Error: {e}")
            self.progress.emit(-1)  # Emit a special value to indicate an error


#####Class Receive Thread##############################################################################################
class ComReceiveThread(QThread):
    def __init__(self, com, textEdit_Receive, Com_Close_Button_clicked, checkBox_HexShow, signal_status_bar,signal_uart_receive):
        super().__init__()
        self.com = com
        self.textBrowser_Receive = textEdit_Receive
        self.Com_Close_Button_clicked = Com_Close_Button_clicked
        self.checkBox_HexShow = checkBox_HexShow
        self.signal_status_bar = signal_status_bar
        self.signal_uart_receive=signal_uart_receive
    def receive_zone_update(self, message):
        self.textBrowser_Receive.insertPlainText(message)
        self.signal_status_bar.emit(message)


    def run(self):
        if self.com.is_open == True:
            try:
                rxData = bytes(self.com.read_all())
            except:
                # QMessageBox.critical(self, 'Fatal error', 'The serial port received wrond data. Please check the serial port connect.')
                # QMessageBox.warning(self, 'Fatal error', 'The serial port received wrond data. Please check the serial port connect.')
                self.Com_Close_Button_clicked()
            if self.checkBox_HexShow.isChecked() == False and rxData != b'':
                self.signal_uart_receive.emit(rxData.decode('UTF-8'))
                self.textBrowser_Receive.insertPlainText(rxData.decode('UTF-8'))
                self.textBrowser_Receive.moveCursor(QTextCursor.End)
            elif self.checkBox_HexShow.isChecked() == True and rxData != b'':
                Data = binascii.b2a_hex(rxData).decode('ascii')
                # re 正则表达式 (.{2}) 匹配两个字母
                hexStr = ' 0x'.join(re.findall('(.{2})', Data))
                # 补齐第一个 0x
                hexStr = '0x' + hexStr
                self.signal_uart_receive.emit(hexStr+' ')
                self.textBrowser_Receive.insertPlainText(hexStr)
                self.textBrowser_Receive.insertPlainText(' ')
                self.textBrowser_Receive.moveCursor(QTextCursor.End)
            elif rxData == b'':
                return None
        else:
            return None




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #PortSelectDialog().listport()
    mainWindow = PortSelectDialog()
    mainWindow.show()
    sys.exit(app.exec_())