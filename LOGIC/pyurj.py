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
            0x800010900E,  # lw s0 0(s0) progbuff0
            0x84004001CE,  # ebreak    progbuff1
            memory_addr_int,  # write address in data 0
            0x5C009C4022,  # copy dato 0 to s0 then exe progbuff0 and progbuff1
            0x5C00884022,  # copy s0 to data0, transfer=1
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
        #print(f"Memory Address {hex_num}: {middle_part_hex}")
        return f"{hex_num}: {middle_part_hex}"
    def lookmem_range(self, memory_addr_start=0x00000000, memory_addr_end=0x00000000):
        current_addr = memory_addr_start
        memory_str =''
        while current_addr <= memory_addr_end:
            memory_str += self.lookmem(current_addr) + '\r'
            current_addr += 4  # 按步长递增
        return memory_str
    def trigger_read(self):
        tselect = self.dmi_instruction_generate(0x2, 0x7A0022F3, 0x20)
        tdata1 = self.dmi_instruction_generate(0x2, 0x7A1022F3, 0x20)
        tdata2 = self.dmi_instruction_generate(0x2, 0x7A2022F3, 0x20)
        tinfo = self.dmi_instruction_generate(0x2, 0x7A4022F3, 0x20)
        cmd = [tselect, tdata1, tdata2, tinfo]
        names = ["tselect", "tdata1", "tdata2", "tinfo"]  # 给每个元素一个名称
        messages=''
        for name, i in zip(names, cmd):
            CMD_TDATAREAD = [
                i,  # csrr x5, tdatareg read tdatareg to x5 progbuff0
                0x84004001CE,  # ebreak    progbuff1
                # 0x84000001CE,  # progbuff1 NOP
                0x5C009C4022,  # copy dato 0 to s0 then exe progbuff0 and progbuff1
                0x5c00884016,  # copy x5 to data0, transfer=1
                0x1000000001,  # read dato0
            ]
            self.urc.set_instruction("DMI")
            self.urc.shift_ir()
            for CMD in CMD_TDATAREAD:
                self.urc.set_dr_in(CMD)
                self.urc.shift_dr()
                self.urc.shift_dr()
            tdata = self.urc.get_dr_out_string()
            decoded_value = self.dmi_instruction_decode(tdata)
            print(f"{name} = {decoded_value}")
            messages+=f"\n{name}={decoded_value}"
        return messages
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
            cmd,  # csrw tdatareg, x5  write x5 to tdatareg progbuff0
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
    def dcsr_read(self):
        dscr_read_cmd=self.dmi_instruction_generate(0x2,0x7B002EF3,0x20)
        CMD_DCSRREAD = [
            dscr_read_cmd, #csrw t4, dcsr x29
            0x84004001CE,  # ebreak    progbuff1
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
        dcsr_value=self.urc.get_dr_out_string()
        # 提取 [8:6] 位
        extracted_bits = dcsr_value[-11:-8]
        dmi_str = self.dmi_instruction_decode(self.urc.get_dr_out_string())
        # 检查提取的位是否为 '000'
        if extracted_bits != '000':
            # 使用 match - case 结构进行匹配
            match extracted_bits:
                case '100':
                    print('dcsr is ',dmi_str,'dcsr.cause - return from single-stepping')
                case '011':
                    print('dcsr is ',dmi_str,'dcsr.cause - external halt request (from DM)')
                case '010':
                    print('dcsr is ',dmi_str,'dcsr.cause - triggered by hardware')
                case '001':
                    print('dcsr is ',dmi_str,'dcsr.cause - executed EBREAK instruction')
        else:
            print('dcsr is ', dmi_str)
            return
        #print('dcsr is ',self.dmi_instruction_decode(self.urc.get_dr_out_string()))
        return dmi_str
    def mstatus_read(self):
        CMD_DCSRREAD = [
            0x80C00A41CE,  # csrw x5, mstatus read mstatus to x5
            0x84004001CE,  # ebreak    progbuff1
            # 0x84000001CE,  #progbuff1 NOP
            0x5C009C4022,  # copy dato 0 to s0 then exe progbuff0 and progbuff1
            0x5c00884016,  # copy x5 to data0, transfer=1
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
    def dcsr_set(self,CMD=None):
        if CMD is None:
            dcsr_data0=0x1100001342 #setp bit =0
        elif CMD == 'STEP':
            dcsr_data0=0x1100001352
        else:
            dcsr_data0=self.dmi_instruction_generate(0x2,CMD,0x04)
            dcsr_set_cmd=self.dmi_instruction_generate(0x2,0x7B002EF3,0x20)
        CMD_STEPSET = [
            #dcsr_set_cmd,
            0x81EC3A41CC, # csrw dcsr, t4
            #0x81EC0A41CE,  # csrw dcsr, x5  write x5 to dcsr
            0x84004001CE,  # ebreak    progbuff1
            dcsr_data0,  # write new dcsr(step=1) in data 0
            # memory_addr_int,
            0x5C009C4076,  # copy dato 0 to t4 then exe progbuff0 and progbuff1
            #0x5C009C4016,  # copy dato 0 to x5 then exe progbuff0 and progbuff1
        ]
        self.urc.set_instruction("DMI")
        self.urc.shift_ir()
        for CMD in CMD_STEPSET:
            self.urc.set_dr_in(CMD)
            self.urc.shift_dr()
            self.urc.shift_dr()
        #print(self.urc.get_dr_out_string())
    def dpc_read(self):
        dpc_read_cmd = self.dmi_instruction_generate(0x2, 0x7B102E73, 0x20)
        CMD_DPCREAD=[
            #0x81EC408BCE,  #csrw x5, dpc read dpc to x5
            dpc_read_cmd, #csrw x28(t3), dpc read dpc to x28
            #0x80D04A41CE,  #csrw x5, mepc read mepc to x5
            #0x800010900E,  # lw s0 0(s0)
            0x84004001CE,  # ebreak    progbuff1
            #memory_addr_int,  # write address in data 0
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
            print('dpc',{CMD},'is ',self.dmi_instruction_decode(self.urc.get_dr_out_string()))
        print('dpc is ',self.dmi_instruction_decode(self.urc.get_dr_out_string()))
        decode_value=self.dmi_instruction_decode(self.urc.get_dr_out_string())
        return decode_value
    def mepc_read(self):
        CMD_MEPCREAD=[
            0x80D04A41CE,  #csrw x5, mepc read mepc to x5
            #0x800010900E,  # lw s0 0(s0)
            0x84004001CE,  # ebreak    progbuff1
            #memory_addr_int,  # write address in data 0
            0x5C009C4022,  # copy dato 0 to s0 then exe progbuff0 and progbuff1
            0x5c00884016,  # copy x5 to data0, transfer=1
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
    def dpc_step(self, dpc_value):
        # 将 dpc_value 转换为整数，增加 4
        dpc_int = int(dpc_value, 16) + 4

        # 将结果转换回 8 位的 16 进制字符串（没有前缀 0x）
        new_dpc = f"{dpc_int:08X}"

        print(dpc_int)  # 打印调试信息
        return dpc_int
    def gpio_read(self):
        gpio_in = 0xfff00000
        gpio_out = 0xfff00004
        cmd = [gpio_in, gpio_out]
        #cmd = [gpio_in]
        names = ["gpio_in", "gpio_out",]# 给每个元素一个名称
        #names = ["gpio_in"]  # 给每个元素一个名称
        s=''
        for name, i in zip(names, cmd):
            s+=f"{name} is\n {self.lookmem(i)[-8:]}\n"
        self.debug_status_detect()
        print(s)
        return s
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
    #Urjtag_T.lookmem(0xfffff7a0)
    Urjtag_T.haltreq()
    #Urjtag_T.dcsr_detect()
    Urjtag_T.gpio_read()
    #Urjtag_T.dcsr_detect()
    Urjtag_T.haltresumereq()
