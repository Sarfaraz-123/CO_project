import sys


def binary_7_bit(number):
    binary_number = bin(number)
    binary_number = binary_number[2::]
    padding = '0' * (7 - len(binary_number))
    result = padding + binary_number
    return result

def binary_8_bit(number):
    binary_number = bin(number)
    binary_number = binary_number[2::]
    paddings = '0' * (8 - len(binary_number))
    result = paddings + binary_number
    return result


def instructions_types(ins, is_Register=-1):
    type_a = ["add", "sub", "mul", "xor", "or", "and"]
    type_b = ["mov", "rs", "ls"]
    type_c = ["mov", "div", "not", "cmp"]
    type_d = ["ld", "st"]
    type_e = ["jmp", "jlt", "jgt", "je"]
    type_f = ["hlt"]

    if is_Register == 0:
        return 'b'
    if is_Register == 1:
        return 'c'

    if ins in type_a:
        return 'a'
    if ins in type_b:
        return 'b'
    if ins in type_c:
        return 'c'
    if ins in type_d:
        return 'd'
    if ins in type_e:
        return 'e'
    if ins in type_f:
        return 'f'

    return -1


def opcode(ins, is_Register=-1):
    opcode_add = "00000"
    opcode_sub = "00001"
    opcode_mov_reg = "00010"
    opcode_mov_imm = "00011"
    opcode_ld = "00100"
    opcode_st = "00101"
    opcode_mul = "00110"
    opcode_div = "00111"
    opcode_rs = "01000"
    opcode_ls = "01001"
    opcode_xor = "01010"
    opcode_or = "01011"
    opcode_and = "01100"
    opcode_not = "01101"
    opcode_cmp = "01110"
    opcode_jmp = "01111"
    opcode_jlt = "10000"
    opcode_jgt = "10001"
    opcode_je = "10010"
    opcode_hlt = "10011"

    if is_Register == 0:
        return opcode_mov_reg
    elif is_Register == 1:
        return opcode_mov_imm

    if ins == "add":
        return opcode_add
    elif ins == "sub":
        return opcode_sub
    elif ins == "mov":
        return opcode_mov_reg
    elif ins == "ld":
        return opcode_ld
    elif ins == "st":
        return opcode_st
    elif ins == "mul":
        return opcode_mul
    elif ins == "div":
        return opcode_div
    elif ins == "rs":
        return opcode_rs
    elif ins == "ls":
        return opcode_ls
    elif ins == "xor":
        return opcode_xor
    elif ins == "or":
        return opcode_or
    elif ins == "and":
        return opcode_and
    elif ins == "not":
        return opcode_not
    elif ins == "cmp":
        return opcode_cmp
    elif ins == "jmp":
        return opcode_jmp
    elif ins == "jlt":
        return opcode_jlt
    elif ins == "jgt":
        return opcode_jgt
    elif ins == "je":
        return opcode_je
    elif ins == "hlt":
        return opcode_hlt

    return None


def register_Address(register):
    register_R0 = '000'
    register_R1 = '001'
    register_R2 = '010'
    register_R3 = '011'
    register_R4 = '100'
    register_R5 = '101'
    register_R6 = '110'
    register_FLAGS = '111'

    if register == 'R0':
        return register_R0
    elif register == 'R1':
        return register_R1
    elif register == 'R2':
        return register_R2
    elif register == 'R3':
        return register_R3
    elif register == 'R4':
        return register_R4
    elif register == 'R5':
        return register_R5
    elif register == 'R6':
        return register_R6
    elif register == 'FLAGS':
        return register_FLAGS

    return -1


# rom helper import *
# from helper import calculate_average
assembly_program = []
# Open the file in read mode
# file = open('assembler_textfile.txt', 'r')
with open("assembler.txt", "r") as file:
    assembly_program = file.readlines()
