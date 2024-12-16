def parse_input(file_path):
    """
    Parse the input file containing the warehouse map and robot movement instructions.

    Args:
        file_path (str): Path to the input file.

    Returns:
        tuple: A tuple containing:
            - tuple: Robot position as (row, col).
            - set of tuple: Wall positions as (row, col).
            - set of tuple: Box positions as (row, col).
            - str: The robot movement instructions as a single concatenated string.
    """
    warehouse_map = []
    movement_instructions = []
    robot_position = None
    wall_positions = set()
    box_positions = set()

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Separate the map and movement instructions
    is_parsing_map = True
    for line in lines:
        stripped_line = line.strip()

        if not stripped_line:  # Skip empty lines
            continue

        if is_parsing_map:
            if stripped_line.startswith('#'):  # Part of the map
                warehouse_map.append(stripped_line)
                for row, line in enumerate(warehouse_map):
                    for col, char in enumerate(line):
                        if char == '#':
                            wall_positions.add((row, col))
                        elif char == 'O':
                            box_positions.add((row, col))
                        elif char == '@':
                            robot_position = (row, col)
            else:  # Movement instructions begin
                is_parsing_map = False
                movement_instructions.append(stripped_line)
        else:
            movement_instructions.append(stripped_line)

    # Join all movement instructions into a single string
    movement_instructions = ''.join(movement_instructions)

    return robot_position, wall_positions, box_positions, movement_instructions


def move(robot_pos, boxes, walls, direction):
    """
    Attempt to move the robot in the given direction. Push a line of boxes if needed.
    """
    dr, dc = direction
    new_robot_pos = (robot_pos[0] + dr, robot_pos[1] + dc)

    # Check if the robot can move
    if new_robot_pos in walls:
        return robot_pos, boxes  # Blocked by a wall, no movement

    # If there's a box (or line of boxes) in the way
    if new_robot_pos in boxes:
        # Identify the line of boxes in the direction
        line_of_boxes = []
        current_box_pos = new_robot_pos
        while current_box_pos in boxes:
            line_of_boxes.append(current_box_pos)
            current_box_pos = (current_box_pos[0] + dr, current_box_pos[1] + dc)

        # Check if the last box in the line can be pushed
        final_box_pos = current_box_pos  # The position after the last box
        if final_box_pos in walls:
            return robot_pos, boxes  # Line cannot be pushed, no movement

        # Push the entire line of boxes
        for box_pos in reversed(line_of_boxes):
            boxes.remove(box_pos)
            boxes.add((box_pos[0] + dr, box_pos[1] + dc))

    # Move the robot
    return new_robot_pos, boxes


def simulate_robot_movements(robot_pos, boxes, walls, instructions):
    """
    Simulate all robot movements based on the instructions.
    """
    directions = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }

    for instruction in instructions:
        robot_pos, boxes = move(robot_pos, boxes, walls, directions[instruction])
    return boxes


def calculate_gps_sum(boxes):
    """
    Calculate the sum of GPS coordinates for all boxes.
    """
    gps_sum = 0
    for box in boxes:
        row, col = box
        gps_sum += 100 * row + col
    return gps_sum


def move_2(robot_pos, direction, grid):
    """
    Attempt to move the robot in the given direction. Push a line of boxes if needed.
    """
    robot_pos += direction
    if all([
        grid[robot_pos] != '[' or move_2(robot_pos + 1, direction, grid) and move_2(robot_pos, direction, grid),
        grid[robot_pos] != ']' or move_2(robot_pos - 1, direction, grid) and move_2(robot_pos, direction, grid),
        grid[robot_pos] != 'O' or move_2(robot_pos, direction, grid), grid[robot_pos] != '#']):
        grid[robot_pos], grid[robot_pos - direction] = grid[robot_pos - direction], grid[robot_pos]
        return True


def part_2(grid, moves):
    grid = grid.translate(str.maketrans({'#': '##', '.': '..', 'O': '[]', '@': '@.'}))

    grid = {i + j * 1j: c for j, r in enumerate(grid.split()) for i, c in enumerate(r)}

    pos, = (p for p in grid if grid[p] == '@')

    for m in moves.replace('\n', ''):
        dir = {'<': -1, '>': +1, '^': -1j, 'v': +1j}[m]
        copy = grid.copy()

        if move_2(pos, dir, grid):
            pos += dir
        else:
            grid = copy

    ans = sum(pos for pos in grid if grid[pos] in 'O[')
    print(int(ans.real + ans.imag * 100))


if __name__ == "__main__":
    file_path = "example_1.txt"  # Replace with your input file path
    robot_pos, walls, boxes, instructions = parse_input(file_path)
    final_boxes = simulate_robot_movements(robot_pos, boxes, walls, instructions)
    gps_sum = calculate_gps_sum(final_boxes)
    print(f"The sum of all boxes' GPS coordinates is: {gps_sum}")

    file_path = "example_2.txt"  # Replace with your input file path
    robot_pos, walls, boxes, instructions = parse_input(file_path)
    final_boxes = simulate_robot_movements(robot_pos, boxes, walls, instructions)
    gps_sum = calculate_gps_sum(final_boxes)
    print(f"The sum of all boxes' GPS coordinates is: {gps_sum}")

    file_path = "input.txt"  # Replace with your input file path
    robot_pos, walls, boxes, instructions = parse_input(file_path)
    final_boxes = simulate_robot_movements(robot_pos, boxes, walls, instructions)
    gps_sum = calculate_gps_sum(final_boxes)
    print(f"The sum of all boxes' GPS coordinates is: {gps_sum}")

    grid, moves = open('input.txt').read().split('\n\n')
    part_2(grid, moves)
