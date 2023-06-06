from sys import stdin

def binary8bitToInt(binaryValue):
    return int(binaryValue, 2)

def intToBinary16bit(value):
    raw_binary = bin(value)[2:].zfill(16)
    return raw_binary

class UniqueMemory:
    data = []

    def initialize(self):
        line = stdin.readline()
        while line:
            self.data.append(line[0:16])
            line = stdin.readline()
        
        if len(self.data) < 128:
            lineDifference = 128 - len(self.data)
            while lineDifference > 0:
                self.data.append("0000000000000000")
                lineDifference -= 1

    def getData(self, currentPC):
        return self.data[currentPC]

    def dump(self):
        for ins in self.data:
            print(ins)

    def getValueFromAddress(self, memoryAddress):
        return int(self.data[binary8bitToInt(memoryAddress)], 2)

    def setValueOfAddress(self, memoryAddress, intValue):
        self.data[binary8bitToInt(memoryAddress)] = intToBinary16bit(intValue)


MEM = UniqueMemory()
