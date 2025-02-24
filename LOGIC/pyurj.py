import sys
from operator import length_hint
import re
from pyexpat.errors import messages

from PyQt5.QtCore import pyqtSignal

sys.path.append('/home/sun/workspace/third/urjtag-git/urjtag/bindings/python/build/lib.linux-x86_64-cpython-312')
from time import sleep
import urjtag  # 现在可以导入 urjtag 了！

class UrjtagTermin():
    signal_connection=pyqtSignal(bool)
    def __init__(self, parent=None):
        self.receive_thread = None
        self.timer = None
        self.urc = None
        # 设置实例
        self.create_items()
        self.preloadcmd()
        # 设置信号与槽
    # 设置实例
    def create_items(self):
        self.urc = urjtag.chain()
        self.connection_detect()
        #self.urc.tap_detect()
    def connection_detect(self):
        if self.urc.cable("dirtyjtag") is not None:
            raise ("Could not connect to JTAG Device. Please reset and try again.")
            return False
        else:
            return True
    def chain_reset(self):
        self.urc.reset()
    def preloadcmd(self):
        self.urc.addpart(5)
        self.urc.part(0)
        self.urc.add_register("IDCODE",32)
        self.urc.add_register("DTMCS",32)
        self.urc.add_register("DMI", 41)
        self.urc.add_instruction("DMI", "10001", "DMI")
        self.urc.add_instruction("IDCODE", "00001", "IDCODE")
        self.urc.add_instruction("DTMCS", "00001", "DTMCS")
    def haltreq(self):
        CMD_HALTREQ_C=0x4200000006
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        self.urc.set_dr_in(CMD_HALTREQ_C)
        self.urc.shift_dr()
        self.urc.shift_dr()
        #print(self.urc.get_dr_out_string())
    def haltresumereq(self):
        CMD_HALTRESUMEREQ_C=0x4100000002
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        self.urc.set_dr_in(CMD_HALTRESUMEREQ_C)
        self.urc.shift_dr()
        self.urc.shift_dr()
        #print(self.urc.get_dr_out_string())

    def reset(self):
        for i in range(1):  # 运行 3 次 (i 从 0 到 2)
            self.urc.set_pod_signal(urjtag.URJ_POD_CS_RESET, 0)
            v = self.urc.get_pod_signal(urjtag.URJ_POD_CS_RESET)
            print(f"Reset cycle {i + 1}, signal state: {v}")  # 添加调试输出
            sleep(1)  # 正确使用 sleep
            self.urc.set_pod_signal(urjtag.URJ_POD_CS_RESET, urjtag.URJ_POD_CS_RESET)
            v = self.urc.get_pod_signal(urjtag.URJ_POD_CS_RESET)
            print(f"Reset cycle {i + 1}, signal state: {v}")  # 添加调试输出
        self.chain_reset()
    def lookreg(self):
        self.haltreq()
        CMD_CPREG2DATA0_C=[
            0x5c00884002,
            0x5c00884006,
            0x5c0088400a,
            0x5c0088400e,
            0x5c00884012,
            0x5c00884016,
            0x5c0088401a,
            0x5c0088401e,
            0x5c00884022,
            0x5c00884026,
            0x5c0088402a,
            0x5c0088402e,
            0x5c00884032,
            0x5c00884036,
            0x5c0088403a,
            0x5c0088403e,
            0x5c00884042,
            0x5c00884046,
            0x5c0088404a,
            0x5c0088404e,
            0x5c00884052,
            0x5c00884056,
            0x5c0088405a,
            0x5c0088405e,
            0x5c00884062,
            0x5c00884066,
            0x5c0088406a,
            0x5c0088406e,
            0x5c00884072,
            0x5c00884076,
            0x5c0088407a,
            0x5c0088407e
        ]
        CMD_READDATA0_C=0x1000000001
        reg_str=''
        for CMD in CMD_CPREG2DATA0_C:
            self.urc.set_instruction("DMI")
            self.urc.shift_ir()
            self.urc.set_dr_in(CMD)
            self.urc.shift_dr()
            self.urc.shift_dr()
            self.urc.set_dr_in(CMD_READDATA0_C)
            self.urc.shift_dr()
            self.urc.shift_dr()
            hex_value_value ='0x'+ self.dmi_instruction_decode(self.urc.get_dr_out_string())
            reg_str+=hex_value_value+' '
        return_value_down = reg_str
        return_value_up = "X00(zero)  X01(ra)    X02(sp)    X03(gp)    X04(tp)    X05(t0)    X06(t1)    X07(t2)    " \
                          "X08(s0/fp) X09(s1)    X10(a0)    X11(a1)    X12(a2)    X13(a3)    X14(a4)    X15(a5)    " \
                          "X16(a6)    X17(a7)    X18(s2)    X19(s3)    X20(s4)    X21(s5)    X22(s6)    X23(s7)    " \
                          "X24(s8)    X25(s9)    X26(s10)   X27(s11)   X28(t3)    X29(t4)    X30(t5)    X31(t6)"
        return_value = return_value_up[0:176]+"\n"+return_value_down[0:176]+"\n"+return_value_up[176:]+"\n"+return_value_down[176:]
        print(return_value)
        return return_value
    def lookmem(self,memory_addr):
        self.haltreq()
        hex_num = hex(memory_addr)[2:].zfill(8)
        memory_addr_int=self.dmi_instruction_generate(0x2,memory_addr,0x04)
        CMD_LOOKMEM = [
            0x80003cbc0e,  # lw t4 0(t4) progbuff0
            0x84004001CE,  # ebreak    progbuff1
            memory_addr_int,  # write address in data 0
            0x5c009c407a, # copy dato 0 to t4 then exe progbuff0 and progbuff1
            0x5c0088407a,   # copy t4 to data0, transfer=1
            0x1000000001,  # read dato0
        ]
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        for CMD in CMD_LOOKMEM:
            #self.lookreg()
            self.urc.set_dr_in(CMD)
            self.urc.shift_dr()
            self.urc.shift_dr()
            # print(self.urc.get_dr_out_string())
        memory_addr_value = self.urc.get_dr_out_string()
        # 提取前 7 位和后 2 位之间的部分
        middle_part_hex = '0x'+self.dmi_instruction_decode(memory_addr_value)
        print(f"Memory Address {hex_num}: {middle_part_hex}")
        return f"{hex_num}: {middle_part_hex}"
    def lookmem_range(self, memory_addr_start=0x00000000, memory_addr_end=0x00000000):
        current_addr = memory_addr_start
        memory_str =''
        while current_addr <= memory_addr_end:
            memory_str += self.lookmem(current_addr) + '\r'
            current_addr += 4  # 按步长递增
        return memory_str
    def setmem(self,address,value):
        self.haltreq()
        hex_num = hex(address)[2:].zfill(8)
        memory_value = self.dmi_instruction_generate(0x2, value, 0x04)
        memory_address=self.dmi_instruction_generate(0x2, address, 0x04)
        operator_cmd=self.dmi_instruction_generate(0x2,0x01EFA023,0x20)
        CMD_LOOKMEM = [
            memory_value,  # write address in data 0
            0x5C008C407A,  # copy dato 0 to t5 and do nothing
            operator_cmd, #sw t5(value) 0(t6)(address) put value in address
            #0x80003cbc0e,  # sw t4 0(t4) progbuff0
            0x84004001CE,  # ebreak    progbuff1
            memory_address,
            0x5C009C407E,  # copy dato 0 to t6 then exe progbuff0 and progbuff1
            0x1000000001,  # read dato0
        ]
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        for CMD in CMD_LOOKMEM:
            # self.lookreg()
            self.urc.set_dr_in(CMD)
            self.urc.shift_dr()
            self.urc.shift_dr()
            # print(self.urc.get_dr_out_string())
        memory_addr_value = self.urc.get_dr_out_string()
        # 提取前 7 位和后 2 位之间的部分
        middle_part_hex = '0x' + self.dmi_instruction_decode(memory_addr_value)
        print(f"Memory Address {address:#x}: is set to {value:#x}")
        return f"{hex_num}: {middle_part_hex}"
    def trigger_model_csr_read(self):
        csrs=[
        # Trigger Module CSR (0x7a0 - 0x7a4)
        (0x7a0, "tselect", "CSR_TSELECT", "Trigger Select Register"),
        (0x7a1, "tdata1", "CSR_TDATA1", "Trigger Data Register 1"),
        (0x7a2, "tdata2", "CSR_TDATA2", "Trigger Data Register 2"),
        (0x7a4, "tinfo", "CSR_TINFO", "Trigger Information Register"),

        # CPU Debug Mode CSR (0x7b0 - 0x7b2)
        (0x7b0, "dcsr", "CSR_DCSR", "Debug Control and Status Register"),
        (0x7b1, "dpc", "CSR_DPC", "Debug Program Counter"),
        (0x7b2, "dscratch0", "CSR_DSCRATCH0", "Debug Scratch Register 0"),

        ]
        messages = ''
        commands = []
        for addr, name_asm, name_c, desc in csrs:
            # self.debug_status_reset()
            instruction = (addr << 20) | 0x2FF3  # 生成 CSR 读取指令
            cmd = self.dmi_instruction_generate(0x2, instruction, 0x20)
            CMD_MCSRREAD = [
                cmd,  # csrr x5, tdatareg read tdatareg to x5 progbuff0
                0x84004001CE,  # ebreak    progbuff1
                # 0x84000001CE,  # progbuff1 NOP
                0x5C009C407E,  # copy dato 0 to t5 then exe progbuff0 and progbuff1
                0x5C0088407E,  # copy t5 to data0, transfer=1
                0x1000000001,  # read dato0
            ]
            self.urc.set_instruction("DMI")
            self.urc.shift_ir()
            for CMD in CMD_MCSRREAD:
                self.urc.set_dr_in(CMD)
                self.urc.shift_dr()
                self.urc.shift_dr()
            tdata = self.urc.get_dr_out_string()
            decoded_value = self.dmi_instruction_decode(tdata)
            #print(f"{name_asm} = {decoded_value}")
            #print(f"{name_asm:<13} = {decoded_value:>9} - {desc}")
            messages += f"\n{name_asm:<13} = {decoded_value:>9}"
            commands.append((addr, name_asm, desc, cmd, decoded_value))
            # if addr == 0x7bc:
            #     self.mcause_read()
            # elif addr == 0x7b0:
            #     messages += f" {self.dcsr_detect(tdata)}"
        commands.append(messages)
        return commands
    def trigger_set(self, address, name=''):
        tselect = self.dmi_instruction_generate(0x2, 0x7A029073, 0x20)
        tdata1 = self.dmi_instruction_generate(0x2, 0x7A129073, 0x20)
        tdata2 = self.dmi_instruction_generate(0x2, 0x7A229073, 0x20)
        tinfo = self.dmi_instruction_generate(0x2, 0x7A029073, 0x20)
        tdata1_set = self.dmi_instruction_generate(0x2, address, 0x04)
        tdata2_set = self.dmi_instruction_generate(0x2, address, 0x04)
        cmds = [tdata1,tdata2]
        names = ["tdata1","tdata2"]  # 给每个元素一个名称
        dmi_instructions=[tdata1_set,tdata2_set]
        if name==names[0]:
            dmi_instruction = dmi_instructions[0]
            cmd=cmds[0]
        elif name==names[1]:
            dmi_instruction = dmi_instructions[1]
            cmd=cmds[1]
        CMD_TDATASET = [
            cmd,  # csrw tdatareg, x5  write x5 to tdatareg progbuff0 7A0E9073 t4
            0x84004001CE,  # ebreak    progbuff1
            dmi_instruction,  # write new dpc in data 0
            # memory_addr_int,
            0x5C009C4016,  # copy dato 0 to x5 then exe progbuff0 and progbuff1
        ]
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        for CMD in CMD_TDATASET:
            self.urc.set_dr_in(CMD)
            self.urc.shift_dr()
            self.urc.shift_dr()
        tdata = self.urc.get_dr_out_string()
        decoded_value = self.dmi_instruction_decode(tdata)
        print(f"{name} is set to {hex(address)}")
        return
    def trigger_tdata1_detect(self):
        csrs=[(0x7a1, "tdata1", "CSR_TDATA1", "Trigger Data Register 1"),]
        messages = ''
        commands = []
        for addr, name_asm, name_c, desc in csrs:
            # self.debug_status_reset()
            instruction = (addr << 20) | 0x2FF3  # 生成 CSR 读取指令
            cmd = self.dmi_instruction_generate(0x2, instruction, 0x20)
            CMD_MCSRREAD = [
                cmd,  # csrr x5, tdatareg read tdatareg to x5 progbuff0
                0x84004001CE,  # ebreak    progbuff1
                # 0x84000001CE,  # progbuff1 NOP
                0x5C009C407E,  # copy dato 0 to t5 then exe progbuff0 and progbuff1
                0x5C0088407E,  # copy t5 to data0, transfer=1
                0x1000000001,  # read dato0
            ]
            self.urc.set_instruction("DMI")
            self.urc.shift_ir()
            for CMD in CMD_MCSRREAD:
                self.urc.set_dr_in(CMD)
                self.urc.shift_dr()
                self.urc.shift_dr()
            tdata = self.urc.get_dr_out_string()
            decoded_value = self.dmi_instruction_decode(tdata)
            messages += f"\n{name_asm:<13} = {decoded_value:>9}"
            commands.append((addr, name_asm, desc, cmd, decoded_value))
        commands.append(messages)
        return commands
    def dcsr_read(self):
        csrs=[(0x7b0, "dcsr", "CSR_DCSR", "Debug Control and Status Register"),]
        messages = ''
        commands = []
        for addr, name_asm, name_c, desc in csrs:
            # self.debug_status_reset()
            instruction = (addr << 20) | 0x2FF3  # 生成 CSR 读取指令
            cmd = self.dmi_instruction_generate(0x2, instruction, 0x20)
            CMD_MCSRREAD = [
                cmd,  # csrr x5, tdatareg read tdatareg to x5 progbuff0
                0x84004001CE,  # ebreak    progbuff1
                # 0x84000001CE,  # progbuff1 NOP
                0x5C009C407E,  # copy dato 0 to t5 then exe progbuff0 and progbuff1
                0x5C0088407E,  # copy t5 to data0, transfer=1
                0x1000000001,  # read dato0
            ]
            self.urc.set_instruction("DMI")
            self.urc.shift_ir()
            for CMD in CMD_MCSRREAD:
                self.urc.set_dr_in(CMD)
                self.urc.shift_dr()
                self.urc.shift_dr()
            tdata = self.urc.get_dr_out_string()
            decoded_value = self.dmi_instruction_decode(tdata)
            messages += f"\n{name_asm:<13} = {decoded_value:>9}"
            commands.append((addr, name_asm, desc, cmd, decoded_value))
        commands.append(messages)
        return commands
    def debug_status_detect(self):
        CMD_ABSTRACT=0x5800000001
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        self.urc.set_dr_in(CMD_ABSTRACT)
        self.urc.shift_dr()
        self.urc.shift_dr()
        abstract_info=self.urc.get_dr_out()
        abstract_info_bin = bin(abstract_info)[2:].zfill(41)
        if abstract_info_bin[0:7] !='0010110':
            print("ERROR - debug status is not found")
        else:
            # 提取 [12:10] 位
            extracted_bits = abstract_info_bin[-13:-10]
            # 检查提取的位是否为 '000'
            if extracted_bits != '000':
                # 使用 match - case 结构进行匹配
                match extracted_bits:
                    case '100':
                        print('ERROR - command cannot be executed since hart is not in expected state')
                    case '011':
                        print('ERROR - exception during command execution')
                    case '010':
                        print('ERROR - unsupported command')
                    case '001':
                        print('ERROR - invalid DM register read/write while command is/was executing')
                return False
            else:
                print("PASS - Debug status detect")
                return True
    def debug_status_reset(self):
        if not self.debug_status_detect():
            CMD_ABSTRACTRESUME_C=0x5808003C06
            self.urc.set_instruction("DMI")
            self.urc.shift_ir()
            self.urc.set_dr_in(CMD_ABSTRACTRESUME_C)
            self.urc.shift_dr()
            self.urc.shift_dr()
            #print(self.urc.get_dr_out_string())
    def dcsr_detect(self,decode_value):
        dcsr_value_bin=bin(int(decode_value,16))
        # 提取 [8:6] 位
        dscr_value_str=str(dcsr_value_bin)[2:].zfill(31)
        extracted_bits = dscr_value_str[-9:-6]

        # 检查提取的位是否为 '000'
        if extracted_bits != '000':
            # 使用 match - case 结构进行匹配
            match extracted_bits:
                case '100':
                    cause_str = 'cause - return from single-stepping'
                    print('dcsr is ',decode_value,'dcsr.cause - return from single-stepping')
                case '011':
                    cause_str = 'cause - return from single-stepping'
                    print('dcsr is ',decode_value,'dcsr.cause - external halt request (from DM)')
                case '010':
                    cause_str = 'cause - return from single-stepping'
                    print('dcsr is ',decode_value,'dcsr.cause - triggered by hardware')
                case '001':
                    cause_str = 'cause - return from single-stepping'
                    print('dcsr is ',decode_value,'dcsr.cause - executed EBREAK instruction')
        else:
            cause = ''
            print('dcsr is ', decode_value)
            return
        #print('dcsr is ',self.dmi_instruction_decode(self.urc.get_dr_out_string()))
        return cause_str
    def mstatus_read(self):
        mstatus_read_cmd = self.dmi_instruction_generate(0x2, 0x30002EF3, 0x20)
        CMD_DCSRREAD = [
            mstatus_read_cmd,  # csrr t4, mstatus read mstatus to x5
            0x84004001CE,  # ebreak    progbuff1
            # 0x84000001CE,  #progbuff1 NOP
            0x5C009C4076,  # copy dato 0 to t4 then exe progbuff0 and progbuff1
            0x5C00884076,   #opy t4 to data0, transfer=1
            0x1000000001,  # read dato0
        ]
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        for CMD in CMD_DCSRREAD:
            self.urc.set_dr_in(CMD)
            self.urc.shift_dr()
            self.urc.shift_dr()
        dmi_str = self.dmi_instruction_decode(self.urc.get_dr_out_string())
        print('mstatus is ', dmi_str)
        return dmi_str
    def mstatus_set(self,CMD=None):
        return
    def mtavl_read(self):
        mtval_read_cmd = self.dmi_instruction_generate(0x2, 0x34302EF3, 0x20)
        CMD_MTVALREAD = [
            mtval_read_cmd,  # csrr t4, mtval read mtval to x5
            0x84004001CE,  # ebreak    progbuff1
            # 0x84000001CE,  #progbuff1 NOP
            0x5C009C4076,  # copy dato 0 to t4 then exe progbuff0 and progbuff1
            0x5C00884076,  # copy t4 to data0, transfer=1
            0x1000000001,  # read dato0
        ]
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        for CMD in CMD_MTVALREAD:
            self.urc.set_dr_in(CMD)
            self.urc.shift_dr()
            self.urc.shift_dr()
        dmi_str = self.dmi_instruction_decode(self.urc.get_dr_out_string())
        print('mtval is ', dmi_str)
        return dmi_str
    def dcsr_set(self,CMD=None):
        if CMD is None:
            dcsr_data0=0x1100001342 #setp bit =0
            action_str = 'Clean step run status'
        elif CMD == 'STEP':
            dcsr_data0=0x1100001352
            action_str = 'Set step run status'
        else:
            dcsr_data0=self.dmi_instruction_generate(0x2,CMD,0x04)
        #dcsr_set_cmd=self.dmi_instruction_generate(0x2,0x7B002EF3,0x20)
        dcsr_set_cmd = self.dmi_instruction_generate(0x2, 0x7B0E9073, 0x20) #csrw dcsr, t6
        CMD_STEPSET = [
            dcsr_set_cmd,
            #0x81EC0A41CE,  # csrw dcsr, x5  write x5 to dcsr
            0x84004001CE,  # ebreak    progbuff1
            dcsr_data0,  # write new dcsr(step=1) in data 0
            # memory_addr_int,
            0x5C009C4076,  # copy dato 0 to t4 then exe progbuff0 and progbuff1
            0x5C00884076,  # copy t4 to data0, transfer=1
            0x1000000001,  # read dato0
        ]
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        for CMD in CMD_STEPSET:
            self.urc.set_dr_in(CMD)
            self.urc.shift_dr()
            self.urc.shift_dr()
        dmi_str = self.dmi_instruction_decode(self.urc.get_dr_out_string())
        print(f"dscr is set to",dmi_str,'-',action_str)
        return dmi_str
    def dpc_read(self):
        dpc_read_cmd = self.dmi_instruction_generate(0x2, 0x7B102E73, 0x20)
        CMD_DPCREAD=[
            dpc_read_cmd, #csrw x28(t3), dpc read dpc to x28
            0x84004001CE,  # ebreak    progbuff1
            0x5C009C4072,  # copy dato 0 to t3 then exe progbuff0 and progbuff1
            0x5C00884072,  # copy t3 to data0
            0x1000000001,  # read dato0
            ]
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        for CMD in CMD_DPCREAD:
            self.urc.set_dr_in(CMD)
            self.urc.shift_dr()
            self.urc.shift_dr()
        print('dpc is ',self.dmi_instruction_decode(self.urc.get_dr_out_string()))
        decode_value=self.dmi_instruction_decode(self.urc.get_dr_out_string())
        return decode_value
    def mepc_read(self):
        mepc_read_cmd=self.dmi_instruction_generate(0x2, 0x34102E73, 0x20)
        CMD_MEPCREAD=[
            mepc_read_cmd,  #csrw t3, mepc read mepc to x3
            #0x800010900E,  # lw s0 0(s0)
            0x84004001CE,  # ebreak    progbuff1
            #memory_addr_int,  # write address in data 0
            0x5C009C4072,  # copy dato 0 to t3 then exe progbuff0 and progbuff1
            0x5C00884072,  # copy t3 to data0
            0x1000000001,  # read dato0
            ]
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        for CMD in CMD_MEPCREAD:
            self.urc.set_dr_in(CMD)
            self.urc.shift_dr()
            self.urc.shift_dr()
        #print(self.urc.get_dr_out_string())
        print('mepc is ',self.dmi_instruction_decode(self.urc.get_dr_out_string()))
        decode_value=self.dmi_instruction_decode(self.urc.get_dr_out_string())
        return decode_value
    def mcause_read(self):
        mcause_read_cmd=self.dmi_instruction_generate(0x2,0x34202E73,0x20)
        CMD_MCAUSEREAD=[
            mcause_read_cmd,    #csrw t3, mcause read mepc to t3
            0x84004001CE,  # ebreak    progbuff1
            #memory_addr_int,  # write address in data 0
            0x5C009C4072,  # copy dato 0 to t3 then exe progbuff0 and progbuff1
            0x5C00884072,  # copy t3 to data0
            0x1000000001,  # read dato0
            ]
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        for CMD in CMD_MCAUSEREAD:
            self.urc.set_dr_in(CMD)
            self.urc.shift_dr()
            self.urc.shift_dr()
        #print(self.urc.get_dr_out_string())
        print('mcause is ',self.dmi_instruction_decode(self.urc.get_dr_out_string()))
        decode_value=self.dmi_instruction_decode(self.urc.get_dr_out_string())

        def detect_mcause(mcause):
            """
            根据输入的 mcause 值查找 NEORV32 Trap 信息，并返回格式化的结果字符串。
            参数：
              mcause: 整型，表示 mcause 的数值。
            返回：
              str，包含对应 Trap 信息的描述；若未找到，则提示未找到。
            """
            mcause_table = [
                {"prio": 1, "mcause": 0x00000001, "trap_id": "TRAP_CODE_I_ACCESS", "cause": "instruction access fault",
                 "mepc": "I-PC", "mtval": 0, "mtinst": "INS"},
                {"prio": 2, "mcause": 0x00000002, "trap_id": "TRAP_CODE_I_ILLEGAL", "cause": "illegal instruction",
                 "mepc": "PC", "mtval": 0, "mtinst": "INS"},
                {"prio": 3, "mcause": 0x00000000, "trap_id": "TRAP_CODE_I_MISALIGNED",
                 "cause": "instruction address misaligned", "mepc": "PC", "mtval": 0, "mtinst": "INS"},
                {"prio": 4, "mcause": 0x0000000b, "trap_id": "TRAP_CODE_MENV_CALL",
                 "cause": "environment call from M-mode", "mepc": "PC", "mtval": 0, "mtinst": "INS"},
                {"prio": 5, "mcause": 0x00000008, "trap_id": "TRAP_CODE_UENV_CALL",
                 "cause": "environment call from U-mode", "mepc": "PC", "mtval": 0, "mtinst": "INS"},
                {"prio": 6, "mcause": 0x00000003, "trap_id": "TRAP_CODE_BREAKPOINT",
                 "cause": "software breakpoint / trigger firing", "mepc": "PC", "mtval": 0, "mtinst": "INS"},
                {"prio": 7, "mcause": 0x00000006, "trap_id": "TRAP_CODE_S_MISALIGNED",
                 "cause": "store address misaligned", "mepc": "PC", "mtval": "ADR", "mtinst": "INS"},
                {"prio": 8, "mcause": 0x00000004, "trap_id": "TRAP_CODE_L_MISALIGNED",
                 "cause": "load address misaligned", "mepc": "PC", "mtval": "ADR", "mtinst": "INS"},
                {"prio": 9, "mcause": 0x00000007, "trap_id": "TRAP_CODE_S_ACCESS", "cause": "store access fault",
                 "mepc": "PC", "mtval": "ADR", "mtinst": "INS"},
                {"prio": 10, "mcause": 0x00000005, "trap_id": "TRAP_CODE_L_ACCESS", "cause": "load access fault",
                 "mepc": "PC", "mtval": "ADR", "mtinst": "INS"},
                # Interrupts
                {"prio": 11, "mcause": 0x80000010, "trap_id": "TRAP_CODE_FIRQ_0",
                 "cause": "fast interrupt request channel 0", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 12, "mcause": 0x80000011, "trap_id": "TRAP_CODE_FIRQ_1",
                 "cause": "fast interrupt request channel 1", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 13, "mcause": 0x80000012, "trap_id": "TRAP_CODE_FIRQ_2",
                 "cause": "fast interrupt request channel 2", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 14, "mcause": 0x80000013, "trap_id": "TRAP_CODE_FIRQ_3",
                 "cause": "fast interrupt request channel 3", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 15, "mcause": 0x80000014, "trap_id": "TRAP_CODE_FIRQ_4",
                 "cause": "fast interrupt request channel 4", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 16, "mcause": 0x80000015, "trap_id": "TRAP_CODE_FIRQ_5",
                 "cause": "fast interrupt request channel 5", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 17, "mcause": 0x80000016, "trap_id": "TRAP_CODE_FIRQ_6",
                 "cause": "fast interrupt request channel 6", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 18, "mcause": 0x80000017, "trap_id": "TRAP_CODE_FIRQ_7",
                 "cause": "fast interrupt request channel 7", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 19, "mcause": 0x80000018, "trap_id": "TRAP_CODE_FIRQ_8",
                 "cause": "fast interrupt request channel 8", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 20, "mcause": 0x80000019, "trap_id": "TRAP_CODE_FIRQ_9",
                 "cause": "fast interrupt request channel 9", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 21, "mcause": 0x8000001a, "trap_id": "TRAP_CODE_FIRQ_10",
                 "cause": "fast interrupt request channel 10", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 22, "mcause": 0x8000001b, "trap_id": "TRAP_CODE_FIRQ_11",
                 "cause": "fast interrupt request channel 11", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 23, "mcause": 0x8000001c, "trap_id": "TRAP_CODE_FIRQ_12",
                 "cause": "fast interrupt request channel 12", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 24, "mcause": 0x8000001d, "trap_id": "TRAP_CODE_FIRQ_13",
                 "cause": "fast interrupt request channel 13", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 25, "mcause": 0x8000001e, "trap_id": "TRAP_CODE_FIRQ_14",
                 "cause": "fast interrupt request channel 14", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 26, "mcause": 0x8000001f, "trap_id": "TRAP_CODE_FIRQ_15",
                 "cause": "fast interrupt request channel 15", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 27, "mcause": 0x8000000b, "trap_id": "TRAP_CODE_MEI",
                 "cause": "machine external interrupt (MEI)", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 28, "mcause": 0x80000003, "trap_id": "TRAP_CODE_MSI",
                 "cause": "machine software interrupt (MSI)", "mepc": "I-PC", "mtval": 0, "mtinst": 0},
                {"prio": 29, "mcause": 0x80000007, "trap_id": "TRAP_CODE_MTI", "cause": "machine timer interrupt (MTI)",
                 "mepc": "I-PC", "mtval": 0, "mtinst": 0},
            ]
            for entry in mcause_table:
                if entry["mcause"] == mcause:
                    result = (
                        f"Prio: {entry['prio']} "
                        f"mcause: 0x{entry['mcause']:08x} "
                        f"Trap ID: {entry['trap_id']} "
                        f"Cause: {entry['cause']} "
                        f"mepc: {entry['mepc']} "
                        f"mtval: {entry['mtval']} "
                        f"mtinst: {entry['mtinst']}"
                    )
                    return result
            return f"未找到对应的 Trap 信息，mcause = 0x{mcause}"

        # 测试该函数
        info = detect_mcause(int(decode_value,16))
        print("查询结果:")
        print(info)
        return decode_value
    def machine_csr_read(self):
        csrs = [
            (0x300, "mstatus", "CSR_MSTATUS", "Machine status register - low word"),
            (0x301, "misa", "CSR_MISA", "Machine CPU ISA and extensions"),
            (0x304, "mie", "CSR_MIE", "Machine interrupt enable register"),
            (0x305, "mtvec", "CSR_MTVEC", "Machine trap-handler base address for ALL traps"),
            # (0x306, "mcounteren", "CSR_MCOUNTEREN", "Machine counter-enable register"),
            (0x310, "mstatush", "CSR_MSTATUSH", "Machine status register - high word"),
            # (0x30A, "menvcfg", "CSR_MENVCFG", "Machine environment configuration register - low word"),
            # (0x31A, "menvcfgh", "CSR_MENVCFGH", "Machine environment configuration register - high word"),
            (0x320, "mcountinhibit", "CSR_MCOUNTINHIBIT", "Machine counter-inhibit register"),
            (0x340, "mscratch", "CSR_MSCRATCH", "Machine scratch register"),
            (0x341, "mepc", "CSR_MEPC", "Machine exception program counter"),
            (0x342, "mcause", "CSR_MCAUSE", "Machine trap cause"),
            (0x343, "mtval", "CSR_MTVAL", "Machine trap value"),
            (0x344, "mip", "CSR_MIP", "Machine interrupt pending register"),
            (0x34A, "mtinst", "CSR_MTINST", "Machine trap instruction")
        ]

        messages = ''
        commands = []
        for addr, name_asm, name_c, desc in csrs:
            #self.debug_status_reset()
            instruction = (addr << 20) | 0x2FF3  # 生成 CSR 读取指令
            cmd = self.dmi_instruction_generate(0x2, instruction, 0x20)
            commands.append((addr, name_asm, name_c, cmd))
            CMD_MCSRREAD = [
                cmd,  # csrr x5, tdatareg read tdatareg to x5 progbuff0
                0x84004001CE,  # ebreak    progbuff1
                # 0x84000001CE,  # progbuff1 NOP
                0x5C009C407E,  # copy dato 0 to t5 then exe progbuff0 and progbuff1
                0x5C0088407E,  # copy t5 to data0, transfer=1
                0x1000000001,  # read dato0
            ]
            self.urc.set_instruction("DMI")
            self.urc.shift_ir()
            for CMD in CMD_MCSRREAD:
                self.urc.set_dr_in(CMD)
                self.urc.shift_dr()
                self.urc.shift_dr()
            tdata = self.urc.get_dr_out_string()
            decoded_value = self.dmi_instruction_decode(tdata)
            #print(f"{name_asm:<13} = {decoded_value:>9} - {desc}")
            messages += f"\n{name_asm:<13} = {decoded_value:>9}"
            if addr == 0x342:
                self.mcause_read()
        commands.append(messages)
        return commands
    def counter_time_csr_read(self):
        messages = ''
        csrs = [
        # Machine Counters and Timers (0xb00 - 0xb82)
        (0xb00, "mcycle", "CSR_MCYCLE", "Machine Cycle Counter Low Word"),
        (0xb02, "minstret", "CSR_MINSTRET", "Machine Instruction Retired Counter Low Word"),
        (0xb80, "mcycleh", "CSR_MCYCLEH", "Machine Cycle Counter High Word"),
        (0xb82, "minstreth", "CSR_MINSTRETH", "Machine Instruction Retired Counter High Word"),

        # User-Level Counters and Timers (0xc00 - 0xc82)
        (0xc00, "cycle", "CSR_CYCLE", "Cycle Counter Low Word"),
        (0xc02, "instret", "CSR_INSTRET", "Instruction Retired Counter Low Word"),
        (0xc80, "cycleh", "CSR_CYCLEH", "Cycle Counter High Word"),
        (0xc82, "instreth", "CSR_INSTRETH", "Instruction Retired Counter High Word"),
        ]
        commands = []
        for addr, name_asm, name_c, desc in csrs:
            if addr == 0x342:
                self.mcause_read()
            else:
                # self.debug_status_reset()
                instruction = (addr << 20) | 0x2FF3  # 生成 CSR 读取指令
                cmd = self.dmi_instruction_generate(0x2, instruction, 0x20)
                commands.append((addr, name_asm, name_c, cmd))
                CMD_MCSRREAD = [
                    cmd,  # csrr x5, tdatareg read tdatareg to x5 progbuff0
                    0x84004001CE,  # ebreak    progbuff1
                    # 0x84000001CE,  # progbuff1 NOP
                    0x5C009C407E,  # copy dato 0 to t5 then exe progbuff0 and progbuff1
                    0x5C0088407E,  # copy t5 to data0, transfer=1
                    0x1000000001,  # read dato0
                ]
                self.urc.set_instruction("DMI")
                self.urc.shift_ir()
                for CMD in CMD_MCSRREAD:
                    self.urc.set_dr_in(CMD)
                    self.urc.shift_dr()
                    self.urc.shift_dr()
                tdata = self.urc.get_dr_out_string()
                decoded_value = self.dmi_instruction_decode(tdata)
                #print(f"{name_asm} = {decoded_value} - {desc}")
                #print(f"{name_asm:<13} = {decoded_value:>9} - {desc}")
                messages += f"\n{name_asm:<13} = {decoded_value:>9}"
        commands.append(messages)
        return commands
    def machine_info_csr_read(self):
        messages = ''
        csrs = [
            (0xf11, "mvendorid", "CSR_MVENDORID"),
            (0xf12, "marchid", "CSR_MARCHID"),
            (0xf13, "mimpid", "CSR_MIMPID"),
            (0xf14, "mhartid", "CSR_MHARTID"),
            (0xf15, "mconfigptr", "CSR_MCONFIGPTR"),
        ]
        commands = []
        for addr, name, desc in csrs:
            if addr == 0x342:
                self.mcause_read()
            else:
                #self.debug_status_reset()
                instruction = (addr << 20) | 0x2FF3  # 生成 CSR 读取指令
                cmd = self.dmi_instruction_generate(0x2, instruction, 0x20)
                commands.append((addr, name, desc, cmd))
                CMD_MCSRREAD = [
                    cmd,  # csrr x5, tdatareg read tdatareg to x5 progbuff0
                    0x84004001CE,  # ebreak    progbuff1
                    # 0x84000001CE,  # progbuff1 NOP
                    0x5C009C407E,  # copy dato 0 to t5 then exe progbuff0 and progbuff1
                    0x5C0088407E,  # copy t5 to data0, transfer=1
                    0x1000000001,  # read dato0
                ]
                self.urc.set_instruction("DMI")
                self.urc.shift_ir()
                for CMD in CMD_MCSRREAD:
                    self.urc.set_dr_in(CMD)
                    self.urc.shift_dr()
                    self.urc.shift_dr()
                tdata = self.urc.get_dr_out_string()
                decoded_value = self.dmi_instruction_decode(tdata)
                #print(f"{name} = {decoded_value}")
                messages += f"\n{name_asm:<13} = {decoded_value:>9}"
        commands.append(messages)
        return commands
    def dpc_set(self,address=None):
        if address is None:
            dpc_step_set=0x1000000002
        elif address == 'STEP' :
            dpc_step=self.dpc_step(self.dpc_read())
            dpc_step_set=self.dmi_instruction_generate(0x2,dpc_step,0x04)
        elif isinstance(address, int) and 0x00000000 <= address <= 0xFFFFFFFF:  # 检查 address 是否是整数并且在有效范围内
            dpc_step_set = self.dmi_instruction_generate(0x2, address, 0x04)  # 使用整数地址生成指令
        else:
            raise ValueError("Invalid address type")  # 处理其他无效的地址类型
        CMD_DPCSET=[
            0x81EC4A41CE,  #csrw dpc, x5  write x5 to dpc
            0x84004001CE,  # ebreak    progbuff1
            dpc_step_set, # write new dpc in data 0
            0x5C009C4016,  # copy dato 0 to x5 then exe progbuff0 and progbuff1
            ]
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        for CMD in CMD_DPCSET:
            self.urc.set_dr_in(CMD)
            self.urc.shift_dr()
            self.urc.shift_dr()
        self.urc.get_dr_out_string()
        address=self.dmi_instruction_decode(dpc_step_set)
        print(f"dpc is set to {hex(address)}")
        self.dpc_read()
    def gpio_read(self):
        gpio_2 = self.dmi_instruction_generate(0x2, 0x00FAF03, 0x20)
        dpc_step_set=self.dmi_instruction_generate(0x2,0xfffffc08,0x04)
        CMD_L=[
            gpio_2, #lw   t5, 0(a0) giop output
            #0x81EC4A41CE,  # csrr a0, data0
            0x84004001CE,  # ebreak    progbuff1
            dpc_step_set,  # gpio address in data 0
            0x5C009C407E,  # copy dato 0 to t6 then exe progbuff0 and progbuff1
            0x5C0088407A,  # copy t5 to data0, transfer=1
            0x1000000001,  # read dato0
            ]
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        for CMD in CMD_L:
            self.urc.set_dr_in(CMD)
            self.urc.shift_dr()
            self.urc.shift_dr()
        print('gpio is ', self.dmi_instruction_decode(self.urc.get_dr_out_string()))
        decode_value = self.dmi_instruction_decode(self.urc.get_dr_out_string())
        return decode_value
    def dret(self):
        CMD_DRET=[
            0x80000001CE, # dret in progbuff0
            0x84004001CE,  # ebreak    progbuff1
            #memory_addr_int,  # write address in data 0
            0x5C009C4022,  # copy dato 0 to s0 then exe progbuff0 and progbuff1
            ]
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        for CMD in CMD_DRET:
            self.urc.set_dr_in(CMD)
            self.urc.shift_dr()
            self.urc.shift_dr()

    def dmi_instruction_generate(self,wn=0x2, data=0x00000000, op=0x04):
        # 确保参数在正确的位宽范围内
        wn &= 0x3  # 2-bit
        data &= 0xFFFFFFFF  # 32-bit
        op &= 0x7F  # 7-bit
        # 组合成 41-bit 二进制数（格式: op(3) + data(32) + wn(1)）
        instruction = (op << 34) | (data << 2) | wn
        #print(f"0x{instruction:010X}")
        return instruction
         # 测试

    def dmi_instruction_decode(self,instruction=None):
        if instruction is None:
            return
        # 确保输入是 41 位二进制字符串
        elif isinstance(instruction, int) and 0x0000000000 <= instruction <= 0x10FFFFFFFFF:
            instruction_bin = bin(instruction)[2:].zfill(41)  # 将整数转换为二进制，并去掉 '0b' 前缀
            extracted_bits = instruction_bin[7:39]             # 提取 第 33-2 位（索引 7 到 39）
            extracted_value_int = int(extracted_bits, 2)             # 转换为整数
            extracted_value_hex = hex(int(extracted_bits, 2))
            print("The instruction is an integer. Binary:", extracted_bits,"hex:",extracted_value_hex)
            return extracted_value_int
        elif isinstance(instruction, str):
            if len(instruction) != 41 or not all(c in "01" for c in instruction):
                raise ValueError("instruction 必须是 41 位的二进制字符串")
                return
            else:
                # 提取 第 33-2 位（索引 7 到 39）
                extracted_bits = instruction[7:39]
                # 转换为整数
                extracted_value = int(extracted_bits, 2)
                return f"{extracted_value:08X}"
    def haltinfo(self):
        CMD_HALTINFO_C=0x4800000001
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        self.urc.set_dr_in(CMD_HALTINFO_C)
        self.urc.shift_dr()
        self.urc.shift_dr()
        print(self.urc.get_dr_out_string())
        print(f'haltinfo is',self.dmi_instruction_decode(self.urc.get_dr_out_string()))
if __name__ == "__main__":
    Urjtag_T=UrjtagTermin()
    #Urjtag_T.reset()
    #Urjtag_T.haltreq()
    Urjtag_T.debug_status_reset()
    #Urjtag_T.debug_status_reset()
    #Urjtag_T.lookreg()
    #Urjtag_T.connection_detect()
    #Urjtag_T.haltresumereq()
    #Urjtag_T.lookmem_range(0x00000000,0x00000040)
    Urjtag_T.haltreq()

    a=Urjtag_T.trigger_tdata1_detect()
    print(a[0][-1])
    #Urjtag_T.gpio_read()
    #Urjtag_T.dcsr_detect()
    Urjtag_T.haltresumereq()
