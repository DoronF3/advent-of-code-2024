def parse_input(file_path):
    """
    Parse the input data into wires and operations.

    Arguments:
        file_path -- Path to the input file.

    Returns:
        wires -- Dictionary with wire names as keys and their values as integers.
        operations -- List of operations as tuples (input1, operation, input2, result).
        highest_z -- The highest 'z' wire name.
    """
    wires = {}
    operations = []
    highest_z = "z00"

    with open(file_path) as f:
        for line in f.read().splitlines():
            if ":" in line:
                wire, value = line.split(": ")
                wires[wire] = int(value)
            elif "->" in line:
                op1, op, op2, _, res = line.split()
                operations.append((op1, op, op2, res))
                if res.startswith("z") and int(res[1:]) > int(highest_z[1:]):
                    highest_z = res

    return wires, operations, highest_z


def process(op, op1, op2):
    """Perform the given binary operation."""
    operations = {
        "AND": lambda x, y: x & y,
        "OR": lambda x, y: x | y,
        "XOR": lambda x, y: x ^ y
    }
    return operations.get(op, lambda x, y: None)(op1, op2)


def evaluate_gates(wire_values, operations):
    """
    Evaluate gates by resolving wire dependencies.

    Arguments:
        wire_values -- Dictionary of wire values.
        operations -- List of operations to evaluate.

    Returns:
        Updated wire_values with evaluated operations.
    """
    unresolved = operations.copy()

    while unresolved:
        for gate in unresolved[:]:
            input1, gate_type, input2, output = gate
            if input1 in wire_values and input2 in wire_values:
                wire_values[output] = process(gate_type, wire_values[input1], wire_values[input2])
                unresolved.remove(gate)

    return wire_values


def calculate_output(wire_values):
    """
    Calculate the final output from wires starting with 'z'.

    Arguments:
        wire_values -- Dictionary of wire values.

    Returns:
        Final output as an integer.
    """
    z_wires = {k: v for k, v in wire_values.items() if k.startswith('z')}
    binary_string = ''.join(str(z_wires[k]) for k in sorted(z_wires.keys(), reverse=True))
    return int(binary_string, 2)


def detect_wrong_operations(operations, highest_z):
    """
    Detect incorrect operations based on the conditions.

    Arguments:
        operations -- List of operations.
        highest_z -- Highest 'z' wire name.

    Returns:
        Set of incorrectly specified wires.
    """
    wrong = set()

    for op1, op, op2, res in operations:
        if res.startswith('z') and op != "XOR" and res != highest_z:
            wrong.add(res)
        if op == "XOR" and all(c[0] not in "xyz" for c in (op1, op2, res)):
            wrong.add(res)
        if op == "AND" and "x00" not in (op1, op2):
            for subop1, subop, subop2, subres in operations:
                if res in (subop1, subop2) and subop != "OR":
                    wrong.add(res)
        if op == "XOR":
            for subop1, subop, subop2, subres in operations:
                if res in (subop1, subop2) and subop == "OR":
                    wrong.add(res)

    return wrong


def evaluate_operations(wires, operations):
    """
    Evaluate operations with dependency resolution.

    Arguments:
        wires -- Dictionary of wire values.
        operations -- List of operations.

    Returns:
        Updated wire dictionary.
    """
    queue = operations.copy()

    while queue:
        op1, op, op2, res = queue.pop(0)
        if op1 in wires and op2 in wires:
            wires[res] = process(op, wires[op1], wires[op2])
        else:
            queue.append((op1, op, op2, res))

    return wires


if __name__ == '__main__':
    # Process multiple files efficiently
    for file_path in ['example_1.txt', 'example_2.txt', 'input.txt']:
        wires, gates, highest_z = parse_input(file_path)
        wires = evaluate_gates(wires, gates)
        result = calculate_output(wires)
        print(f"{file_path} Output: {result}")

    # Detect wrong operations
    wires, operations, highest_z = parse_input("input.txt")
    wrong = detect_wrong_operations(operations, highest_z)
    wires = evaluate_operations(wires, operations)
    print(",".join(sorted(wrong)))
