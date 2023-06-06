def intToBinary8bit(value):
    raw_binary = bin(value)[2:].zfill(8)
    return raw_binary

def intToBinary77bit(value):
    raw_binary = bin(value)[2:].zfill(7)
    return raw_binary


class UniqueProgramCounter:
    current_counter = 0

    def initialize(self):
        self.current_counter = 0

    def getValue(self):
        return self.current_counter

    def update(self, new_counter):
        self.current_counter = new_counter

    def dump(self):
        print(intToBinary77bit(self.current_counter), end="        ")

PC = UniqueProgramCounter()