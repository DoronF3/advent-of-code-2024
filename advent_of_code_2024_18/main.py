from collections import deque


def read_input_file(file_path):
    """Reads the input file and parses the falling byte positions."""
    with open(file_path, 'r') as file:
        return [(int(x), int(y)) for line in file for x, y in [line.strip().split(',')]]


def bfs_shortest_path(grid_size, falling_bytes_set, start, end):
    """Finds the shortest path using BFS with falling bytes set as obstacles."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    queue = deque([(start[0], start[1], 0)])  # (x, y, steps)
    visited = set([start])

    while queue:
        x, y, steps = queue.popleft()

        if (x, y) == end:
            return steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < grid_size and 0 <= ny < grid_size and (nx, ny) not in visited:
                if (nx, ny) not in falling_bytes_set:  # Check if the byte has fallen at this position
                    visited.add((nx, ny))
                    queue.append((nx, ny, steps + 1))

    return -1  # Return -1 if no path is found


def find_blocking_byte(grid_size, falling_bytes, time, falling_bytes_set):
    """Finds the byte that blocks the exit by simulating the falling bytes."""
    while True:
        falling_bytes_set.add(falling_bytes[time])

        # Check the shortest path for this time step
        result = bfs_shortest_path(grid_size, falling_bytes_set, (0, 0), (grid_size - 1, grid_size - 1))
        if result == -1:  # If no path is found, the byte at this time is blocking the exit
            return falling_bytes[time]  # Return the blocking byte position
        time += 1


def process_input(file_path, grid_size, time):
    """Reads the input, simulates falling bytes, and finds the shortest path and blocking byte."""
    falling_bytes = read_input_file(file_path)

    # Calculate the shortest path
    falling_bytes_set = set(falling_bytes[:time])  # Only store bytes up to the given time
    shortest_path_length = bfs_shortest_path(grid_size, falling_bytes_set, (0, 0), (grid_size - 1, grid_size - 1))
    print(f"The minimum number of steps needed to reach the exit is: {shortest_path_length}")

    # Find the blocking byte
    blocking_byte = find_blocking_byte(grid_size, falling_bytes, time, falling_bytes_set)
    print(f"The byte blocking the exit is at: {blocking_byte}")


if __name__ == "__main__":
    # Configuration for the first input
    process_input("example_1.txt", 7, 12)

    # Configuration for the second input
    process_input("input.txt", 71, 1024)
