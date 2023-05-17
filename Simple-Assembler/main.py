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
for kx in sys.stdin:
    assembly_program.append(kx)
# Read the contents of the file
# text = file.readlines()


# for line in sys.stdin:
# for line in sys.text:
    # if(line):
    # ith index of the list represents the (i+1)th line of the assembly code
    # assembly_program.append(line)

converted_Binary = []  # append the result statements to be printed in this list
errors_Faced = []  # append any encountered errors to this list


halt_Faced = False
labels = dict()
variables = dict()
variable_Declarations_Now = True

var_Lines = 0
index = 0

while index < len(assembly_program):
    line = assembly_program[index]

    if not line:
        index += 1
        continue
    elif line.split()[0] == "var":
        var_Lines += 1
        index += 1
    else:
        break


blank_Lines = 0
for line in assembly_program:
    if (not line):
        blank_Lines += 1


temp_var_Lines = var_Lines
next_variable_location = len(assembly_program) - var_Lines - blank_Lines
line_number = 1

for _ in range(var_Lines):
    current_line = assembly_program[0]
    is_blank_line = not current_line.strip()

    if is_blank_line:
        line_number += 1
        continue

    line_tokens = current_line.split()
    operation = line_tokens[0]

    if operation == "var" and len(line_tokens) == 2:
        var_declaration = line_tokens[1]
        is_new_variable = var_declaration not in variables.keys()

        if is_new_variable:
            new_variable_value = binary_7_bit(next_variable_location)
            variables[var_declaration] = new_variable_value
            next_variable_location += 1
            var_Lines -= 1
            assembly_program.pop(0)
            line_number += 1
            continue
        else:
            error_message = f"ERROR at Line {line_number}: Multiple declarations for the same variable found"
            errors_Faced.append(error_message)
            line_number += 1
            continue

    elif operation == "var":
        error_message = f"ERROR at Line {line_number}: Improper variable declaration"
        errors_Faced.append(error_message)
        var_Lines -= 1
        assembly_program.pop(0)
        line_number += 1
        continue

    else:
        variable_Declarations_Now = False
        break

variable_Declarations_Now = False
var_Lines = temp_var_Lines


for line_Number, line in enumerate(assembly_program):
    if not line:
        continue

    current_Line = line.split()
    if current_Line[0][-1] == ":":
        label = current_Line[0][:-1]
        if label not in labels:
            labels[label] = binary_8_bit(line_Number)
            assembly_program[line_Number] = ' '.join(current_Line[1:])
        else:
            errors_Faced.append(
                f"ERROR at Line {line_Number + var_Lines + 1}: Multiple declarations for the same label found")
            continue
for line_Number, line in enumerate(assembly_program):
    current_Line = line.split()

    if not current_Line:
        continue

    if current_Line[0] == "var" and not variable_Declarations_Now:
        errors_Faced.append(
            f"ERROR at Line {line_Number + var_Lines + 1}: Variable not declared at the beginning")
        continue

    if current_Line[0][-1] == ":":
        errors_Faced.append(
            f"ERROR at Line {line_Number + var_Lines + 1}: Use of multiple labels is not supported")
        continue

    if halt_Faced and current_Line[0] != "mov":
        errors_Faced.append(
            f"ERROR at Line {line_Number + var_Lines + 1}: Halt (hlt) not being used as the last instruction")
        continue

    if instructions_types(current_Line[0]) == -1 and current_Line[0] != "mov":
        errors_Faced.append(
            f"ERROR at Line {line_Number + var_Lines + 1}: Invalid instruction")
        continue


    if current_Line[0] == "mov":
        if len(current_Line) == 3:
            if register_Address(current_Line[2]) != -1:
                # mov reg1 reg2
                if register_Address(current_Line[1]) == -1 or register_Address(current_Line[2]) == -1:
                    errors_Faced.append(
                        f"ERROR at Line {line_Number + var_Lines + 1}: Invalid Register")
                    continue
                if register_Address(current_Line[1]) == "111":
                    errors_Faced.append(
                        f"ERROR at Line {line_Number + var_Lines + 1}: Illegal use of FLAGS")
                    continue
                converted_Binary.append(opcode(current_Line[0], 1) + "00000" +
                                    register_Address(current_Line[1]) + register_Address(current_Line[2]))
                continue
            elif current_Line[2][1:].isdecimal():
                # mov reg1 $Imm
                if current_Line[2][0] != "$":
                    errors_Faced.append(
                        f"ERROR at Line {line_Number + var_Lines + 1}: Syntax Error")
                    continue
                if register_Address(current_Line[1]) == -1:
                    errors_Faced.append(
                        f"ERROR at Line {line_Number + var_Lines + 1}: Invalid Register")
                    continue
                if register_Address(current_Line[1]) == "111":
                    errors_Faced.append(
                        f"ERROR at Line {line_Number + var_Lines + 1}: Illegal use of FLAGS")
                    continue
                if int(current_Line[2][1:]) < 0 or int(current_Line[2][1:]) > 255:
                    errors_Faced.append(
                        f"ERROR at Line {line_Number + var_Lines + 1}: Illegal Immediate Value")
                    continue
                converted_Binary.append(opcode(current_Line[0], 0) + "0" +
                                    register_Address(current_Line[1]) + binary_7_bit(int(current_Line[2][1:])))
                continue
        else:
            errors_Faced.append(
                f"ERROR at Line {line_Number + var_Lines + 1}: Wrong Syntax used for instruction")
            continue

    instruction_type = instructions_types(current_Line[0])
    line_number = line_Number + var_Lines + 1

    if instruction_type == 'a' and len(current_Line) == 4:
        reg1 = register_Address(current_Line[1])
        reg2 = register_Address(current_Line[2])
        reg3 = register_Address(current_Line[3])

        if reg1 == -1 or reg2 == -1 or reg3 == -1:
            errors_Faced.append(
                f"ERROR at Line {line_number}: Invalid Register")
            continue
        if reg1 == "111" or reg2 == "111" or reg3 == "111":
            errors_Faced.append(
                f"ERROR at Line {line_number}: Illegal use of FLAGS")
            continue

        converted_Binary.append(opcode(current_Line[0]) + "00" + reg1 + reg2 + reg3)
        continue
    elif instruction_type == 'a':
        errors_Faced.append(
            f"ERROR at Line {line_number}: Wrong Syntax used for instruction")
        continue
    instruction_type = instructions_types(current_Line[0])
    line_number = line_Number + var_Lines + 1

    if instruction_type == 'b' and len(current_Line) == 3:
        immediate_value = current_Line[2][1:]
        reg1 = register_Address(current_Line[1])

        if current_Line[2][0] != "$":
            errors_Faced.append(
                f"ERROR at Line {line_number}: Syntax Error - Invalid immediate value format. Use '$' prefix.")
            continue
        if int(immediate_value) not in range(0, 256):
            errors_Faced.append(
                f"ERROR at Line {line_number}: Illegal Immediate Value - Value must be in the range of 0 to 255.")
            continue
        if reg1 == -1:
            errors_Faced.append(
                f"ERROR at Line {line_number}: Invalid Register - The specified register does not exist.")
            continue
        if reg1 == "111":
            errors_Faced.append(
                f"ERROR at Line {line_number}: Illegal use of FLAGS - Register FLAGS cannot be used in this context.")
            continue

        converted_Binary.append(opcode(current_Line[0]) + "0" + reg1 + binary_7_bit(int(immediate_value)))
        continue
    elif instruction_type == 'b':
        errors_Faced.append(
            f"ERROR at Line {line_number}: Wrong Syntax used for instruction - The specified instruction type 'b' is not valid in this context.")
        continue


    line_number = line_Number + var_Lines + 1

    if instructions_types(current_Line[0]) == 'c' and len(current_Line) == 3:
        instruction = current_Line[0]
        reg1 = current_Line[1]
        reg2 = current_Line[2]
        
        reg1_address = register_Address(reg1)

        reg2_address = register_Address(reg2)

        if reg1_address == -1 or reg2_address == -1:

            errors_Faced.append(

                f"ERROR at Line {line_number}: Invalid Register - One or more registers are invalid.")

            continue

        if reg1_address == "111" or reg2_address == "111":

            errors_Faced.append(

                f"ERROR at Line {line_number}: Illegal use of FLAGS - FLAGS register cannot be used in this context.")

            continue

        converted_Binary.append(opcode(instruction) + "00000" + reg1_address + reg2_address)

        continue

    elif instructions_types(current_Line[0]) == 'c':

        errors_Faced.append(

            f"ERROR at Line {line_number}: Wrong Syntax used for instruction - The specified instruction type 'c' is not valid in this context.")

        continue

    if instructions_types(current_Line[0]) == 'd' and len(current_Line) == 3:

        instruction = current_Line[0]

        reg1 = current_Line[1]

        variable = current_Line[2]

        reg1_address = register_Address(reg1)

        if reg1_address == -1:

            errors_Faced.append(

                f"ERROR at Line {line_number}: Invalid Register - The specified register is invalid.")

            continue

        if reg1_address == "111":

            errors_Faced.append(

                f"ERROR at Line {line_number}: Illegal use of FLAGS - FLAGS register cannot be used in this context.")

            continue

        if variable not in variables.keys():

            if variable in labels.keys():

                errors_Faced.append(

                    f"ERROR at Line {line_number}: Misuse of label as variable - The specified variable '{variable}' is actually a label.")

            else:

                errors_Faced.append(

                    f"ERROR at Line {line_number}: Use of undefined variable - The specified variable '{variable}' is not defined.")

        converted_Binary.append(opcode(instruction) + '0' + reg1_address + variables.get(variable, ''))

        continue

    elif instructions_types(current_Line[0]) == 'd':

        errors_Faced.append(

            f"ERROR at Line {line_number}: Wrong Syntax used for instruction - The specified instruction type 'd' is not valid in this context.")

        continue

    line_number = line_Number + var_Lines + 1

    

    if (instructions_types(current_Line[0]) == 'e' and len(current_Line) == 2):

        ins = current_Line.pop(0)

        if (current_Line[0] not in labels.keys()):

            if (current_Line[0] in variables.keys()):

                errors_Faced.append(

                    "ERROR at Line " + str(line_Number + var_Lines + 1) + ": Misuse of variable as label")

                continue

            else:

                errors_Faced.append(

                    "ERROR at Line " + str(line_Number + var_Lines + 1) + ": Use of undefined labels")

                continue

        else:

            if ins == "je":

                converted_Binary.append(

                    "11111" + '0' * 3 + labels[current_Line[0]])

            elif ins == "jlt":

                converted_Binary.append(

                    "11100" + '0' * 3 + labels[current_Line[0]])

            elif ins == "jgt":

                converted_Binary.append(

                    "11101" + '0' * 3 + labels[current_Line[0]])

            elif ins == "jmp":

                converted_Binary.append(

                    "01111" + '0' * 3 + labels[current_Line[0]])

            else:

                errors_Faced.append(

                    "ERROR at Line " + str(line_Number + var_Lines + 1) + ": Wrong Syntax used for instruction")

                continue

    if instructions_types(current_Line[0]) == 'f':

        instruction = current_Line[0]

        converted_Binary.append("11010" + "00000000000")

        halt_Faced = True

        continue

    elif instructions_types(current_Line[0]) == 'f':

        errors_Faced.append(

            f"ERROR at Line {line_number}: Wrong Syntax used for instruction - The specified instruction type '{instruction}' is not valid in this context.")

        continue

if not halt_Faced:

    errors_Faced.append("ERROR: No halt (hlt) instruction found")

code_length = len(converted_Binary)

if code_length > 256:

    errors_Faced.append("ERROR: The code length exceeds the maximum capacity (256 lines)")

if len(errors_Faced):

    for error in errors_Faced:

        print(error)

else:

  
        for i, binary_16_bit in enumerate(converted_Binary):

            line_number = line_Number + var_Lines + i + 1

            sys.stdout.write(f"{binary_16_bit}\n")

#Thank You..here ends the code

