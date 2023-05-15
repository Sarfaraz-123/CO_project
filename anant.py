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
        print(f"{binary_16_bit}")
