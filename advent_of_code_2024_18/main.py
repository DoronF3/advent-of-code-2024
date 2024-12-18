from collections import deque


def read_input_file(file_path):
    """Reads the input file and parses the falling byte positions."""
    falling_bytes = []
    with open(file_path, 'r') as file:
        for line in file:
            x, y = map(int, line.strip().split(','))
            falling_bytes.append((x, y))
    return falling_bytes


def simulate_falling_bytes(grid_size, falling_bytes, time):
    """Simulates the falling bytes and marks the grid."""
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    for i in range(time):
        grid[falling_bytes[i][1]][falling_bytes[i][0]] = '#'
    return grid


def bfs_shortest_path(grid, start, end):
    """Finds the shortest path using BFS."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    queue = deque([(start[0], start[1], 0)])  # (x, y, steps)
    visited = set()
    visited.add(start)

    while queue:
        x, y, steps = queue.popleft()

        if (x, y) == end:
            return steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < len(grid) and 0 <= ny < len(grid) and (nx, ny) not in visited:
                if grid[ny][nx] == '.':  # Only move to safe cells
                    visited.add((nx, ny))
                    queue.append((nx, ny, steps + 1))

    return -1  # Return -1 if no path is found


def find_blocking_byte(grid_size, falling_bytes, time):
    result = 0
    while result != -1:
        time += 1
        grid = simulate_falling_bytes(grid_size, falling_bytes, time)
        result = bfs_shortest_path(grid, (0, 0), (grid_size - 1, grid_size - 1))
    return falling_bytes[time - 1][0], falling_bytes[time - 1][1]


if __name__ == "__main__":
    # Configuration
    file_path = "example_1.txt"  # Replace with your input file path
    grid_size = 7  # 0 to 70 inclusive
    time = 12

    # Read input and simulate
    falling_bytes = read_input_file(file_path)
    grid = simulate_falling_bytes(grid_size, falling_bytes, time)

    # Calculate the shortest path
    shortest_path_length = bfs_shortest_path(grid, (0, 0), (grid_size - 1, grid_size - 1))
    print(f"The minimum number of steps needed to reach the exit is: {shortest_path_length}")

    # Find the blocking byte
    blocking_byte = find_blocking_byte(grid_size, falling_bytes, time)
    print(f"The byte blocking the exit is at: {blocking_byte}")

    file_path = "input.txt"  # Replace with your input file path
    grid_size = 71  # 0 to 70 inclusive
    time = 1024

    # Read input and simulate
    falling_bytes = read_input_file(file_path)
    grid = simulate_falling_bytes(grid_size, falling_bytes, time)

    # Calculate the shortest path
    shortest_path_length = bfs_shortest_path(grid, (0, 0), (grid_size - 1, grid_size - 1))
    print(f"The minimum number of steps needed to reach the exit is: {shortest_path_length}")

    # Find the blocking byte
    blocking_byte = find_blocking_byte(grid_size, falling_bytes, time)
    print(f"The byte blocking the exit is at: {blocking_byte}")
