
# rom helper import *
# from helper import calculate_average
assembly_program = []
# Open the file in read mode
# file = open('assembler_textfile.txt', 'r')
with open("assembler.txt", "r") as file:
    assembly_program = file.readlines()
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
