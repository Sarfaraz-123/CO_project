def intToBinary16bit(value):
    rawBinary = bin(value)[2:].zfill(16)
    return rawBinary

def checkOverflow(value):
    if value > (2 ** 16 - 1):
        return True
    else:
        return False

class UniqueRegisters:
    registers = {
        "000": 0,  # R0
        "001": 0,  # R1
        "010": 0,  # R2
        "011": 0,  # R3
        "100": 0,  # R4
        "101": 0,  # R5
        "110": 0,  # R6
    }
    flagRegister = "0000000000000000"  # FLAGS

    def resetFlagRegister(self):
        self.flagRegister = "0000000000000000"

    def setOverflowFlag(self):
        self.flagRegister = "0000000000001000"

    def setLessThanFlag(self):
        self.flagRegister = "0000000000000100"

    def setGreaterThanFlag(self):
        self.flagRegister = "0000000000000010"

    def setEqualsFlag(self):
        self.flagRegister = "0000000000000001"

    def printFlag(self):
        print(self.flagRegister, end=" ")

    def setRegister(self, registerAddress, value):
        if not checkOverflow(value):
            self.registers[registerAddress] = value
        else:
            rawBinary = bin(value)[2:].zfill(16)
            self.registers[registerAddress] = int(rawBinary[-16:], 2)

    def getRegister(self, registerAddress, binaryOrDecimal):
        if binaryOrDecimal:
            if registerAddress == "111":
                return self.flagRegister
            rawBinary = bin(self.registers[registerAddress])[2:].zfill(16)
            return rawBinary[-16:]
        else:
            if registerAddress == "111":
                return int(self.flagRegister, 2)
            return self.registers[registerAddress]

    def dump(self):
        for key in self.registers.keys():
            print(intToBinary16bit(self.registers[key]), end=" ")
        print(self.flagRegister)


RF = UniqueRegisters()


    
