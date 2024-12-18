def parse_input(input_file):
    """
    Parses the input file and returns the initial registers and the program.

    Args:
    - input_file (str): Path to the input file.

    Returns:
    - (tuple): A tuple containing:
        - register_a (int): Initial value of register A.
        - register_b (int): Initial value of register B.
        - register_c (int): Initial value of register C.
        - program (list): List of instructions (opcodes and operands).
    """
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Parse the initial register values, stripping out the labels
    register_a = int(lines[0].split(":")[1].strip())  # Extract number after "Register A:"
    register_b = int(lines[1].split(":")[1].strip())  # Extract number after "Register B:"
    register_c = int(lines[2].split(":")[1].strip())  # Extract number after "Register C:"

    # Parse the program (instructions)
    program = list(map(int, lines[4].strip().split(": ")[1].split(",")))  # Instructions start from the fourth line

    return register_a, register_b, register_c, program


def get_operand_value(opcode, operand, register_a, register_b, register_c):
    """
    Returns the value of the operand based on the opcode and whether it's a literal or combo operand.

    Args:
    - opcode (int): The opcode of the instruction.
    - operand (int): The operand value.
    - register_a (int): The value of register A.
    - register_b (int): The value of register B.
    - register_c (int): The value of register C.

    Returns:
    - (int): The resolved operand value.
    """
    if opcode == 0 or opcode == 2 or opcode == 5 or opcode == 6 or opcode == 7:
        # For these opcodes, operand is treated as a combo operand
        if operand <= 3:
            return operand  # Combo operand 0-3 represent literal values 0-3
        elif operand == 4:
            return register_a  # Combo operand 4 represents Register A
        elif operand == 5:
            return register_b  # Combo operand 5 represents Register B
        elif operand == 6:
            return register_c  # Combo operand 6 represents Register C
        else:
            raise ValueError(f"Invalid combo operand: {operand}")
    else:
        # For other opcodes, operand is a literal operand
        return operand  # Literal operand


def run_program_logic(register_a, register_b, register_c, program):
    """
    Executes the program logic using the provided registers and program.

    Args:
    - register_a (int): Value of register A.
    - register_b (int): Value of register B.
    - register_c (int): Value of register C.
    - program (list): List of instructions (opcodes and operands).

    Returns:
    - str: The final output joined by commas.
    """
    # Initialize the instruction pointer and the list to collect outputs
    ip = 0  # Instruction pointer
    output = []  # List to collect the output values

    while ip < len(program):
        # Read the current instruction and its operand
        opcode = program[ip]
        operand = program[ip + 1]

        # Get the value of the operand
        operand_value = get_operand_value(opcode, operand, register_a, register_b, register_c)

        if opcode == 0:  # adv instruction
            register_a = register_a >> operand_value  # Division by 2^operand_value
        elif opcode == 1:  # bxl instruction
            register_b ^= operand_value
        elif opcode == 2:  # bst instruction
            register_b = operand_value % 8
        elif opcode == 3:  # jnz instruction
            if register_a != 0:
                ip = operand_value
                continue  # Skip the default instruction pointer increment
        elif opcode == 4:  # bxc instruction
            register_b ^= register_c
        elif opcode == 5:  # out instruction
            output.append(operand_value % 8)
        elif opcode == 6:  # bdv instruction
            register_b = register_a >> operand_value  # Division by 2^operand_value
        elif opcode == 7:  # cdv instruction
            register_c = register_a >> operand_value  # Division by 2^operand_value

        # Increment instruction pointer (unless we performed a jump)
        ip += 2

    # Return the output as a string joined by commas
    return output


input_file = "input.txt"
register_a, register_b, register_c, program = parse_input(input_file)
target = program[::-1]


def find_a(a=0, depth=0):
    if depth == len(target):
        return a
    for i in range(8):
        output = run_program_logic(a * 8 + i, register_b, register_c, program)
        if output and output[0] == target[depth]:
            if result := find_a((a * 8 + i), depth + 1):
                return result
    return 0


if __name__ == "__main__":
    input_file = "example_1.txt"  # The file containing the input
    register_a, register_b, register_c, program = parse_input(input_file)
    output = run_program_logic(register_a, register_b, register_c, program)
    print(",".join(map(str, output)))

    input_file = "input.txt"  # The file containing the input
    register_a, register_b, register_c, program = parse_input(input_file)
    output = run_program_logic(register_a, register_b, register_c, program)
    print(",".join(map(str, output)))

    print(find_a())
