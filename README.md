# CO_project
ISA Description:
-------------------------
Opcode  Instruction  Semantics                                Syntax            Type
------------------------------------------------------------------------------------- 
10101   Remainder    reg1 = reg2 % reg3                       mod reg1 reg2 reg3   A
10110   Increment    reg1 = reg1 + 1                          inc reg1             C
10111   Decrement    reg1 = reg1 - 1                          dec reg1             C
11011   Negative     reg1 = -reg2                             neg reg1 reg2        D
11110   Swap         swap the values of reg1 and reg2         swap reg1 reg2       D


Binary Encoding:
-------------------------
Type A: 3 register type
-------------------------
Opcode (5 bits)  Unused (2 bits)  reg1 (3 bits)  reg2 (3 bits)  reg3 (3 bits)
-----------------------------------------------------------------------------
  5                 2                3             3             3

Type C: 2 registers type
-------------------------
Opcode (5 bits)  Unused (8 bits)  reg1 (3 bits)  
-------------------------------------------------
5                8                 3              

Type D: register and memory address type
----------------------------------------
Opcode (5 bits)  Unused (5 bit)  reg1 (3 bits) reg2 (3 bits)
---------------------------------------------------------------------
5                 5              3               3
