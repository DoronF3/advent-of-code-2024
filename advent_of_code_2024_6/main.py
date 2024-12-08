def load_grid_from_file(filename):
    """Load grid data from a file."""
    with open(filename, 'r') as file:
        return [list(line.strip()) for line in file]


def find_start_pos_obstacles(grid, start_char='^', obstacle_char='#'):
    """
    Find start positions and obstacles in the grid.

    Args:
        grid: The 2D grid.
        start_char: Character representing the start position.
        obstacle_char: Character representing obstacles.

    Returns:
        A tuple of (start_positions, obstacles).
    """
    start_positions = []
    obstacles = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == start_char:
                start_positions.append((i, j))
            elif cell == obstacle_char:
                obstacles.append((i, j))
    return start_positions, obstacles


def find_distinct_pos(start_pos, obstacles, grid):
    distinct_pos = 0
    guard_pos = start_pos[0]
    visited = []
    direction = (-1, 0)

    while 0 <= guard_pos[0] < len(grid) and 0 <= guard_pos[1] < len(grid[0]):
        if guard_pos not in visited:
            visited.append(guard_pos)
            distinct_pos += 1
        if (guard_pos[0] + direction[0], guard_pos[1] + direction[1]) not in obstacles:
            guard_pos = (guard_pos[0] + direction[0], guard_pos[1] + direction[1])
        else:
            direction = rotate(direction)

    return distinct_pos, visited


def rotate(direction):
    """
    Rotate the direction 90 degrees clockwise.

    Args:
        direction: A tuple representing the current direction.

    Returns:
        A tuple representing the rotated direction.
    """
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left
    current_idx = directions.index(direction)
    return directions[(current_idx + 1) % 4]


def add_obstruction(start_pos, obstacles, grid, visited):
    """
    Count potential obstruction positions that create a loop.

    Args:
        start_pos: The start position of the guard.
        obstacles: Existing obstacles in the grid.
        grid: The 2D grid.

    Returns:
        The number of obstruction options.
    """
    obstruction_options = 0

    for location in visited:
        if grid[location[0]][location[1]] == '.':
            if create_loop(start_pos, obstacles + [location], grid):
                obstruction_options += 1
    return obstruction_options


def create_loop(start_pos, obstacles, grid):
    guard_pos = start_pos[0]
    visited = set()  # Use a set for efficient membership checks
    direction = (-1, 0)  # Initial direction: Up
    visited.add((guard_pos, direction))  # Add the initial state to visited

    rows, cols = len(grid), len(grid[0])  # Cache grid dimensions for boundary checks

    while 0 <= guard_pos[0] < rows and 0 <= guard_pos[1] < cols:
        # Compute the next position
        next_pos = (guard_pos[0] + direction[0], guard_pos[1] + direction[1])

        if next_pos not in obstacles:  # Move if the next position is not an obstacle
            guard_pos = next_pos
        else:  # Rotate direction if blocked
            direction = rotate(direction)

        state = (guard_pos, direction)  # Current state (position + direction)
        if state not in visited:  # Check if state is already visited
            visited.add(state)  # Mark as visited
        else:  # Loop detected
            return True

    return False


if __name__ == '__main__':
    grid = load_grid_from_file('example_1.txt')
    start_pos, obstacles = find_start_pos_obstacles(grid)
    print(find_distinct_pos(start_pos, obstacles, grid)[0])

    grid = load_grid_from_file('input.txt')
    start_pos, obstacles = find_start_pos_obstacles(grid)
    print(find_distinct_pos(start_pos, obstacles, grid)[0])

    grid = load_grid_from_file('example_1.txt')
    start_pos, obstacles = find_start_pos_obstacles(grid)
    visited = find_distinct_pos(start_pos, obstacles, grid)[1]
    print(add_obstruction(start_pos, obstacles, grid, visited))

    grid = load_grid_from_file('input.txt')
    start_pos, obstacles = find_start_pos_obstacles(grid)
    visited = find_distinct_pos(start_pos, obstacles, grid)[1]
    print(add_obstruction(start_pos, obstacles, grid, visited))
