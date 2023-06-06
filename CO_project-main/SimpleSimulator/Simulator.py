from EXECUTION_ENGINE import EE
from MEMORY import MEM
from PROGRAM_COUNTER import PC
from REGISTER import RF


MEM.initialize()
PC.initialize()
halted = False

while(not halted):
    instruction = MEM.getData(PC.getValue())
    halted, newPC = EE.execute(instruction)
    PC.dump()
    RF.dump()
    PC.update(newPC)

MEM.dump()
