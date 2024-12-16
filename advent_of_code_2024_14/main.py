def parse_input(file_path):
    """Parse the input file and return a dictionary of robot positions and speeds."""
    robots = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip():
                pos, speed = line.split()
                x, y = map(int, pos[2:].split(","))
                vx, vy = map(int, speed[2:].split(","))
                robots.append(((x, y), (vx, vy)))
    return robots


def count_robots_in_quadrants(robots, grid_size, steps):
    """
    Count the number of robots in each quadrant and calculate the safety factor.

    Parameters:
    robots (dict): A dictionary where keys are positions (x, y) and values are (dx, dy) speeds.
    grid_size (tuple): The size of the grid (width, height).
    steps (int): The number of time steps to simulate.

    Returns:
    int: The safety factor (product of robot counts in each quadrant).
    """
    width, height = grid_size
    mid_x, mid_y = width // 2, height // 2

    # Initialize quadrant counts
    quadrants = [0, 0, 0, 0]

    for (x, y), (dx, dy) in robots:
        # Calculate final position after 'steps' iterations
        final_x = (x + dx * steps) % width
        final_y = (y + dy * steps) % height

        # Ignore robots on mid-lines
        if final_x == mid_x or final_y == mid_y:
            continue

        # Determine which quadrant the robot is in
        if final_x < mid_x and final_y < mid_y:
            quadrants[0] += 1  # Top-left
        elif final_x >= mid_x and final_y < mid_y:
            quadrants[1] += 1  # Top-right
        elif final_x < mid_x and final_y >= mid_y:
            quadrants[2] += 1  # Bottom-left
        else:
            quadrants[3] += 1  # Bottom-right

    # Calculate safety factor as the product of counts in each quadrant
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


from statistics import variance as var


def find_tree(W, H, robots):
    # Find the time `t` that minimizes variance in x and y directions
    bx = min(range(W), key=lambda t: var((s + t * v) % W for ((s, _), (v, _)) in robots))
    by = min(range(H), key=lambda t: var((s + t * v) % H for ((_, s), (_, v)) in robots))

    # Compute the result
    return bx + ((pow(W, -1, H) * (by - bx)) % H) * W


# Example usage
if __name__ == "__main__":
    input_file = "example_1.txt"
    robots = parse_input(input_file)
    grid_size = (11, 7)
    steps = 100  # Number of steps to simulate
    safety_factor = count_robots_in_quadrants(robots, grid_size, steps)
    print(f"Safety factor after {steps} seconds: {safety_factor}")

    input_file = "input.txt"
    robots = parse_input(input_file)
    grid_size = (101, 103)
    steps = 100  # Number of steps to simulate
    safety_factor = count_robots_in_quadrants(robots, grid_size, steps)
    print(f"Safety factor after {steps} seconds: {safety_factor}")

    input_file = "input.txt"
    robots = parse_input(input_file)
    grid_size = (101, 103)
    steps = 100  # Number of steps to simulate
    print(f"Time to find the tree: {find_tree(*grid_size, robots)}")
