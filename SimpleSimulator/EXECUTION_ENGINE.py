from REGISTER import RF
from MEMORY import MEM
from PROGRAM_COUNTER import PC
def checkOverflow(value):
    '''
    Checks if the value exceeds the range of the registers or not i.e. is it greater than (2^16-1)
    \n\tvalue: An integer value to be passed. The value stored in the register
    \n\tReturns a boolean: True-> overflow      False-> No Overflow
    '''
    if(value > (2**16 - 1)):
        return True
    else:
        return False
def binary8bitToInt(binaryValue):
    '''
    Converts 8bit binary strings to their respective integer values
    '''
    return int(binaryValue, 2)
def binary7bitToInt(binaryValue):
    '''
    Converts 7-bit binary strings to their respective integer values
    '''
    return int(binaryValue, 2)

def intToBinary8bit(value):
    '''
    Exclusively used for Program Counnter (PC)
    '''
    rawBinary = bin(value)[2::]
    length = len(rawBinary)
    binary = '0' * (8 - length) + rawBinary
    return binary

class ExecutionEngine:
    
    def execute(self, instruction):
        '''
        This function takes a 16bit binary string of assembly instructions and returns
        \t(The updated state of the halted instruction, 
        \tThe updated value of the program counter)
        '''
        opcode = instruction[:5:]

        

        if(opcode == "00000"):
            # add unused reg1 reg2 reg3
            # 5   2      3    3    3
            reg1 = instruction[ 7:10:]      # reading address of reg1
            reg2 = instruction[10:13:]      # reading address of reg2
            reg3 = instruction[13:16:]      # reading address of reg3
            res = RF.getRegister(reg2, False) + RF.getRegister(reg3, False)
            if(checkOverflow(res)):
                RF.setOverflowFlag()
            else:
                RF.resetFlagRegister()
            RF.setRegister(reg1, res)
            (halt, newPC) = (False, PC.getValue() + 1)
        # ........................................................................................................................

        elif(opcode == "00001"):
            # sub unused reg1 reg2 reg3
            # 5   2      3    3    3
            reg1 = instruction[ 7:10:]      # reading address of reg1
            reg2 = instruction[10:13:]      # reading address of reg2
            reg3 = instruction[13:16:]      # reading address of reg3
            res = RF.getRegister(reg2,False) - RF.getRegister(reg3,False)
            if (res < 0):
                RF.setOverflowFlag()
                RF.setRegister(reg1,0)
            else:
                RF.setRegister(reg1,res)
                RF.resetFlagRegister()
            (halt, newPC) = (False, PC.getValue() + 1)
        # ........................................................................................................................

        elif opcode == "00010":
                # mov reg1 $Imm
                # 5   3    8
                reg1 =  instruction[6:9]        # reading address of reg1
                value = instruction[9:]        # reading the value of $Imm and setting the unused bit to 1
                value = binary8bitToInt(value)    # adjusting the memory address to 7 bits
                RF.setRegister(reg1, value)
                RF.resetFlagRegister()
                halt = False
                newPC = PC.getValue() + 1

        # ........................................................................................................................

        elif(opcode == "00011"):
            # mov unused reg1 reg2
            # 5   5      3    3
            reg1 = instruction[10:13:]      # reading the address of reg1
            reg2 = instruction[13::]        # reading the address of reg2
            RF.setRegister(reg1, RF.getRegister(reg2, False))
            RF.resetFlagRegister()
            (halt, newPC) = (False, PC.getValue() + 1)
        # ........................................................................................................................

        elif(opcode == "00100"):
    # ld reg1 mem_addr
    # 5  3    8
            reg1 = instruction[6:9:]
            memoryAddress = instruction[9::]
            valueAtMemory = MEM.getValueFromAddress(memoryAddress)
            RF.setRegister(reg1, valueAtMemory)
            RF.resetFlagRegister()
            (halt, newPC) = (False, PC.getValue() + 1)
# ........................................................................................................................

        elif(opcode == "00101"):
            # st reg1 mem_addr
            # 5  3    8
            reg1 =  instruction[6:9:] 
            memoryAddress =  instruction[9::]
            MEM.setValueOfAddress(memoryAddress, RF.getRegister(reg1, False))
            RF.resetFlagRegister()
            (halt, newPC) = (False, PC.getValue() + 1)

        # ........................................................................................................................

        elif(opcode == "00110"):
            # mul unused reg1 reg2 reg3
            # 5   2      3    3    3
            reg1 = instruction[ 7:10:]      # reading address of reg1
            reg2 = instruction[10:13:]      # reading address of reg2
            reg3 = instruction[13:16:]      # reading address of reg3
            res = RF.getRegister(reg2, False) * RF.getRegister(reg3, False)
            if(checkOverflow(res)):
                RF.setOverflowFlag()
            else:
                RF.resetFlagRegister()
            RF.setRegister(reg1, res)
            (halt, newPC) = (False, PC.getValue() + 1)
        # ........................................................................................................................

        elif opcode == "00111":
            # div unused reg3 reg4
            # 5   5      3    3   
            reg3 = instruction[10:13]      # Reading address of reg3
            reg4 = instruction[13:]        # Reading address of reg4

            divisor = RF.getRegister(reg4, False)
            if divisor != 0:
                remainder = RF.getRegister(reg3, False) % divisor
                quotient = RF.getRegister(reg3, False) // divisor
            else:
                remainder = 0
                quotient = 0
                

            RF.setRegister("000", quotient)
            RF.setRegister("111", remainder)
            RF.resetFlagRegister()
            newPC = PC.getValue() + 1
            halt = True 

        # ........................................................................................................................

        elif(opcode == "01000"):
            # rs reg1 $Imm
            # 5  3    8
            reg1 = instruction[5:8:]
            immediateValue = binary8bitToInt(instruction[8::])
            shiftedString = '0' * immediateValue + RF.getRegister(reg1, True)[:len(RF.getRegister(reg1, True)) - immediateValue:]
            RF.setRegister(reg1, int(shiftedString, 2))
            RF.resetFlagRegister()
            (halt, newPC) = (False, PC.getValue() + 1)
        # ........................................................................................................................

        elif(opcode == "01001"):
            # ls reg1 $Imm
            # 5  3    8
            reg1 = instruction[5:8:]
            immediateValue = binary8bitToInt(instruction[8::])
            shiftedString = RF.getRegister(reg1, True)[immediateValue::] + '0' * immediateValue
            RF.setRegister(reg1, int(shiftedString, 2))
            RF.resetFlagRegister()
            (halt, newPC) = (False, PC.getValue() + 1)
        # ........................................................................................................................

        elif(opcode == "01010"):
            # xor unused reg1 reg2 reg3
            # 5   2      3    3    3
            reg1 = instruction[ 7:10:]      # reading address of reg1
            reg2 = instruction[10:13:]      # reading address of reg2
            reg3 = instruction[13:16:]      # reading address of reg3
            res = RF.getRegister(reg2,False) ^ RF.getRegister(reg3,False)
            RF.setRegister(reg1,res)
            RF.resetFlagRegister()
            (halt, newPC) = (False, PC.getValue() + 1)
        # ........................................................................................................................

        elif(opcode == "01011"):
            # or unused reg1 reg2 reg3
            # 5  2      3    3    3
            reg1 = instruction[ 7:10:]      # reading address of reg1
            reg2 = instruction[10:13:]      # reading address of reg2
            reg3 = instruction[13:16:]      # reading address of reg3
            res = RF.getRegister(reg2,False) | RF.getRegister(reg3,False)
            RF.setRegister(reg1,res)
            RF.resetFlagRegister()
            (halt, newPC) = (False, PC.getValue() + 1)
        # ........................................................................................................................

        elif(opcode == "01100"):
            # and unused reg1 reg2 reg3
            # 5   2      3    3    3
            reg1 = instruction[ 7:10:]      # reading address of reg1
            reg2 = instruction[10:13:]      # reading address of reg2
            reg3 = instruction[13:16:]      # reading address of reg3
            res = RF.getRegister(reg2,False) & RF.getRegister(reg3,False)
            RF.setRegister(reg1,res)
            RF.resetFlagRegister()
            (halt, newPC) = (False, PC.getValue() + 1)
        # ........................................................................................................................

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
        # ........................................................................................................................

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
        # ........................................................................................................................

        elif(opcode == "01111"):
             
            if RF.flagRegister == "0000000000000100":
                memoryAddress = instruction[9::]
                (halt, newPC) = (False, binary8bitToInt(memoryAddress))
            else:
                (halt, newPC) = (False, PC.getValue() + 1)
            RF.resetFlagRegister()
        # ........................................................................................................................

        elif(opcode == "11100"):
            # jlt unused mem_addr
            # 5   3      8
            if RF.flagRegister == "0000000000000100":
                memoryAddress = instruction[9::]
                (halt, newPC) = (False, binary8bitToInt(memoryAddress))
            else:
                (halt, newPC) = (False, PC.getValue() + 1)
            RF.resetFlagRegister()
        # ........................................................................................................................

        elif(opcode == "11101"):
            # jgt unused mem_addr
            # 5   3      8
            if RF.flagRegister == "0000000000000010":
                memoryAddress = instruction[9::]
                (halt, newPC) = (False, binary8bitToInt(memoryAddress))
            else:
                (halt, newPC) = (False, PC.getValue() + 1)
            RF.resetFlagRegister()
        # ........................................................................................................................

        elif(opcode == "11111"):
            # je unused mem_addr
            # 5  3      8
            if RF.flagRegister == "0000000000000001":
                memoryAddress = instruction[9::]
                (halt, newPC) = (False, binary8bitToInt(memoryAddress))
            else:
                (halt, newPC) = (False, PC.getValue() + 1)
            RF.resetFlagRegister()
        # ........................................................................................................................

        elif(opcode == "11010"):
            # hlt unused
            # 5   11
            RF.resetFlagRegister()
            (halt, newPC) = (True, PC.getValue() + 1)
        # ........................................................................................................................

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
        # ....................................................
        elif(opcode == "10110"):
            # inc unused reg1
            # 5    8    3
            reg1 = instruction[5:8]      # reading address of reg1
            RF.setRegister(reg1, RF.getRegister(reg1, False) + 1)
            RF.resetFlagRegister()
            (halt, newPC) = (False, PC.getValue() + 1)
        # ........................................................................................................................

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
        # ........................................................................................................................

        return (halt, newPC)
        

EE = ExecutionEngine()