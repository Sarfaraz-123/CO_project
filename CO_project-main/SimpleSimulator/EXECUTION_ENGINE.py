from REGISTER import RF
from MEMORY import MEM
from PROGRAM_COUNTER import PC


def checkOverflow(value):
    if value > (2**16 - 1):
        return True
    else:
        return False


def binary8bitToInt(binaryValue):
    return int(binaryValue, 2)


def intToBinary8bit(value):
    rawBinary = bin(value)[2:]
    length = len(rawBinary)
    binary = '0' * (8 - length) + rawBinary
    return binary


class ExecutionEngine:
    
    def execute(self, instruction):
        opcode = instruction[:5]

        if opcode == "00000":
            reg1_address = instruction[7:10]
            reg2_address = instruction[10:13]
            reg3_address = instruction[13:16]
            result = RF.getRegister(reg2_address, False) + RF.getRegister(reg3_address, False)
            if checkOverflow(result):
                RF.setOverflowFlag()
            else:
                RF.resetFlagRegister()
            RF.setRegister(reg1_address, result)
            halt = False
            newPC = PC.getValue() + 1

        elif opcode == "00001":
            reg1_address = instruction[7:10]
            reg2_address = instruction[10:13]
            reg3_address = instruction[13:16]
            result = RF.getRegister(reg2_address, False) - RF.getRegister(reg3_address, False)
            if result < 0:
                RF.setOverflowFlag()
                RF.setRegister(reg1_address, 0)
            else:
                RF.setRegister(reg1_address, result)
                RF.resetFlagRegister()
            halt = False
            newPC = PC.getValue() + 1

        elif opcode == "00010":
            reg1_address = instruction[6:9]
            value = instruction[9:]
            value = binary8bitToInt(value)
            RF.setRegister(reg1_address, value)
            RF.resetFlagRegister()
            halt = False
            newPC = PC.getValue() + 1

        elif opcode == "00011":
            reg1_address = instruction[10:13]
            reg2_address = instruction[13:]
            RF.setRegister(reg1_address, RF.getRegister(reg2_address, False))
            RF.resetFlagRegister()
            halt = False
            newPC = PC.getValue() + 1

        elif opcode == "00100":
            reg1_address = instruction[5:8]
            memory_address = instruction[8:]
            value_at_memory = MEM.getValueFromAddress(memory_address)
            RF.setRegister(reg1_address, value_at_memory)
            RF.resetFlagRegister()
            halt = False
            newPC = PC.getValue() + 1

        elif opcode == "00101":
            reg1_address = instruction[6:9]
            memory_address = instruction[9:]
            MEM.setValueOfAddress(memory_address, RF.getRegister(reg1_address, False))
            RF.resetFlagRegister()
            halt = False
            newPC = PC.getValue() + 1

        elif opcode == "00110":
            reg1_address = instruction[7:10]
            reg2_address = instruction[10:13]
            reg3_address = instruction[13:16]
            result = RF.getRegister(reg2_address, False) * RF.getRegister(reg3_address, False)
            if checkOverflow(result):
                RF.setOverflowFlag()
            else:
                RF.resetFlagRegister()
            RF.setRegister(reg1_address, result)
            halt = False
            newPC = PC.getValue() + 1

       

        elif opcode == "01000":
            # rs reg1 $Imm
            # 5  3    8
            reg1_addr = instruction[5:8]
            immediate_value = binary8bit_to_int(instruction[8:])
            shifted_string = '0' * immediate_value + register_file.get_register(reg1_addr, True)[:len(register_file.get_register(reg1_addr, True)) - immediate_value]
            register_file.set_register(reg1_addr, int(shifted_string, 2))
            register_file.reset_flag_register()
            halt = False
            new_PC = program_counter.get_value() + 1

        elif opcode == "01001":
            # ls reg1 $Imm
            # 5  3    8
            reg1_addr = instruction[5:8]
            immediate_value = binary8bit_to_int(instruction[8:])
            shifted_string = register_file.get_register(reg1_addr, True)[immediate_value:] + '0' * immediate_value
            register_file.set_register(reg1_addr, int(shifted_string, 2))
            register_file.reset_flag_register()
            halt = False
            new_PC = program_counter.get_value() + 1

        elif opcode == "01010":
            # xor unused reg1 reg2 reg3
            # 5   2      3    3    3
            reg1_addr = instruction[7:10]   # reading address of reg1
            reg2_addr = instruction[10:13]  # reading address of reg2
            reg3_addr = instruction[13:16]  # reading address of reg3
            result = register_file.get_register(reg2_addr, False) ^ register_file.get_register(reg3_addr, False)
            register_file.set_register(reg1_addr, result)
            register_file.reset_flag_register()
            halt = False
            new_PC = program_counter.get_value() + 1

        elif opcode == "01011":
            # or unused reg1 reg2 reg3
            # 5  2      3    3    3
            reg1_addr = instruction[7:10]   # reading address of reg1
            reg2_addr = instruction[10:13]  # reading address of reg2
            reg3_addr = instruction[13:16]  # reading address of reg3
            result = register_file.get_register(reg2_addr, False) | register_file.get_register(reg3_addr, False)
            register_file.set_register(reg1_addr, result)
            register_file.reset_flag_register()
            halt = False
            new_PC = program_counter.get_value() + 1

        elif opcode == "01100":
            # and unused reg1 reg2 reg3
            # 5   2      3    3    3
            reg1_addr = instruction[7:10]   # reading address of reg1
            reg2_addr = instruction[10:13]  # reading address of reg2
            reg3_addr = instruction[13:16]  # reading address of reg3
            result = register_file.get_register(reg2_addr, False) & register_file.get_register(reg3_addr, False)
            register_file.set_register(reg1_addr, result)
            register_file.reset_flag_register()
            halt = False
            new_PC = program_counter.get_value() + 1
           
        elif(opcode == "01101"):
            # not unused reg1 reg2
            # 5   5      3    3
            reg1 = instruction[10:13:]      # Reading address of reg1
            reg2 = instruction[13::]        # Reading address of reg2
            inverted = ""
            for bit in reg2:
                if bit=='1':
                    inverted += '0'
                else:
                    inverted += '1'
            RF.setRegister(reg1, int(inverted, 2))
            RF.resetFlagRegister()
            (halt, newPC) = (False, PC.getValue() + 1)
        

        elif(opcode == "01110"):
            # cmp unused reg1 reg2
            # 5   5      3    3
            reg1 = instruction[10:13:]      # reading address of reg1
            reg2 = instruction[13::]        # reading address of reg2
            if RF.getRegister(reg1, False) < RF.getRegister(reg2, False):
                RF.setLessThanFlag()
            elif RF.getRegister(reg1, False) > RF.getRegister(reg2, False):
                RF.setGreaterThanFlag()
            else:
                RF.setEqualsFlag()
            (halt, newPC) = (False, PC.getValue() + 1)
      
        elif(opcode == "01111"):
            # jmp unused mem_addr
            # 5   3      8
            memoryAddress = instruction[8::]
            (halt, newPC) = (False, binary8bitToInt(memoryAddress))
            RF.resetFlagRegister()
        
        elif(opcode == "11100"):
            # jlt unused mem_addr
            # 5   3      8
            if RF.flagRegister == "0000000000000100":
                memoryAddress = instruction[8::]
                (halt, newPC) = (False, binary8bitToInt(memoryAddress))
            else:
                (halt, newPC) = (False, PC.getValue() + 1)
            RF.resetFlagRegister()
       
        elif(opcode == "11101"):
            # jgt unused mem_addr
            # 5   3      8
            if RF.flagRegister == "0000000000000010":
                memoryAddress = instruction[8::]
                (halt, newPC) = (False, binary8bitToInt(memoryAddress))
            else:
                (halt, newPC) = (False, PC.getValue() + 1)
            RF.resetFlagRegister()
       
        elif(opcode == "11111"):
            # je unused mem_addr
            # 5  3      8
            if RF.flagRegister == "0000000000000001":
                memoryAddress = instruction[8::]
                (halt, newPC) = (False, binary8bitToInt(memoryAddress))
            else:
                (halt, newPC) = (False, PC.getValue() + 1)
            RF.resetFlagRegister()
      

        elif(opcode == "11010"):
            # hlt unused
            # 5   11
            RF.resetFlagRegister()
            (halt, newPC) = (True, PC.getValue() + 1)
       
        elif opcode == "10101":
            # mod unused reg1 reg2 reg3
            # 5   2      3    3    3
            reg1 = instruction[7:10]       # Reading address of reg1
            reg2 = instruction[10:13]      # Reading address of reg2
            reg3 = instruction[13:]        # Reading address of reg3

            dividend = RF.getRegister(reg2, False)
            divisor = RF.getRegister(reg3, False)
            
            if divisor == 0:
                RF.setOverflowFlag()
                RF.setRegister(reg1, 0)
            else:
                quotient = dividend % divisor
                RF.resetFlagRegister()
                RF.setRegister(reg1, quotient)
            
            (halt, newPC) = (False, PC.getValue() + 1)
        
        elif(opcode == "10110"):
            # inc unused reg1
            # 5    8    3
            reg1 = instruction[5:8]      # reading address of reg1
            RF.setRegister(reg1, RF.getRegister(reg1, False) + 1)
            RF.resetFlagRegister()
            (halt, newPC) = (False, PC.getValue() + 1)
       
        elif(opcode == "10111"):
            # dec unused reg1
            # 5    8    3
            reg1 = instruction[5:8]      # reading address of reg1
            RF.setRegister(reg1, RF.getRegister(reg1, False) - 1)
            RF.resetFlagRegister()
            (halt, newPC) = (False, PC.getValue() + 1)
            
        elif opcode == "11011":
            # neg unused reg1 reg2
            # 5   5      3    3
            reg1 = instruction[10:13]      # Reading address of reg1
            reg2 = instruction[13:]        # Reading address of reg2
            res = -RF.getRegister(reg2, False)
            if checkOverflow(res):
                RF.setOverflowFlag()
            else:
                RF.resetFlagRegister()
            RF.setRegister(reg1, res)
            (halt, newPC) = (False, PC.getValue() + 1)

        elif opcode == "11110":
            # swap unused reg1 reg2
            # 5   5      3    3
            reg1 = instruction[10:13]      # Reading address of reg1
            reg2 = instruction[13:]        # Reading address of reg2
            temp = RF.getRegister(reg1, False)
            RF.setRegister(reg1, RF.getRegister(reg2, False))
            RF.setRegister(reg2, temp)
            RF.resetFlagRegister()
            (halt, newPC) = (False, PC.getValue() + 1)
        elif opcode == "10000":
            # F_Addition: Performs reg1 = reg2 + reg3
            # If the computation overflows, the overflow flag is set and reg1 is set to 0
            reg1 = instruction[7:10]      # Reading address of reg1
            reg2 = instruction[10:13]     # Reading address of reg2
            reg3 = instruction[13:16]      # Reading address of reg3
            sum_result = RF.getRegister(reg2, False) + RF.getRegister(reg3, False)
            if checkOverflow(sum_result):
                RF.setOverflowFlag()
                RF.setRegister(reg1, 0)
            else:
                RF.resetFlagRegister()
                RF.setRegister(reg1, sum_result)
            (halt, newPC) = (False, PC.getValue() + 1)

        elif opcode == "10001":
            # F_Subtraction: Performs reg1 = reg2 - reg3
            # If reg3 > reg2, 0 is written to reg1 and the overflow flag is set
            reg1 = instruction[7:10]      # Reading address of reg1
            reg2 = instruction[10:13]     # Reading address of reg2
            reg3 = instruction[13:16]      # Reading address of reg3
            sub_result = RF.getRegister(reg2, False) - RF.getRegister(reg3, False)
            if RF.getRegister(reg3, False) > RF.getRegister(reg2, False):
                RF.setOverflowFlag()
                RF.setRegister(reg1, 0)
            else:
                RF.resetFlagRegister()
                RF.setRegister(reg1, sub_result)
            (halt, newPC) = (False, PC.getValue() + 1)

        elif opcode == "10010":
            # Move F_Immediate: Performs reg1 = $Imm, where Imm is an 8-bit floating-point value
            reg1 = instruction[5:8]      # Reading address of reg1
            immediate_value = instruction[8:]     # Reading the immediate value
            reg1_value = binary_to_float_8bit(immediate_value)   # Converting the immediate value to float
            RF.setRegister(reg1, reg1_value)
            RF.resetFlagRegister()
            (halt, newPC) = (False, PC.getValue() + 1)


        return (halt, newPC)
        

EE = ExecutionEngine()