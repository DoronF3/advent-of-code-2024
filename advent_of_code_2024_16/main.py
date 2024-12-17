import heapq
from collections import deque

# Directions: (dx, dy) for North, East, South, West
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def parse_input(grid):
    start, end = None, None
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'S':
                start = (x, y)
            elif cell == 'E':
                end = (x, y)
    return start, end


def solve_maze(grid):
    start, end = parse_input(grid)
    rows, cols = len(grid), len(grid[0])

    # Priority queue for Dijkstra's algorithm
    pq = []
    heapq.heappush(pq, (0, start[0], start[1], 1))  # (score, x, y, direction)
    visited = set()

    while pq:
        score, x, y, direction = heapq.heappop(pq)

        # If we reach the end
        if (x, y) == end:
            return score

        # Mark current state as visited
        if (x, y, direction) in visited:
            continue
        visited.add((x, y, direction))

        # Move forward
        dx, dy = DIRECTIONS[direction]
        nx, ny = x + dx, y + dy
        if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] != '#':
            heapq.heappush(pq, (score + 1, nx, ny, direction))

        # Rotate left (counterclockwise)
        new_direction = (direction - 1) % 4
        heapq.heappush(pq, (score + 1000, x, y, new_direction))

        # Rotate right (clockwise)
        new_direction = (direction + 1) % 4
        heapq.heappush(pq, (score + 1000, x, y, new_direction))


def read_grid_from_file(file_path):
    """Reads the maze grid from a file."""
    with open(file_path, 'r') as file:
        grid = [line.strip() for line in file.readlines()]
    return grid


def dijkstra(grid, starts):
    delta = {"E": (0, 1), "W": (0, -1), "N": (-1, 0), "S": (1, 0)}

    dist = {}
    pq = []
    for sr, sc, dir in starts:
        dist[(sr, sc, dir)] = 0
        heapq.heappush(pq, (0, sr, sc, dir))

    while pq:
        (score, x, y, direction) = heapq.heappop(pq)
        if dist[(x, y, direction)] < score:
            continue
        for next_dir in "EWNS".replace(direction, ""):
            if (x, y, next_dir) not in dist or dist[(x, y, next_dir)] > score + 1000:
                dist[(x, y, next_dir)] = score + 1000
                heapq.heappush(pq, (score + 1000, x, y, next_dir))
        dx, dy = delta[direction]
        nx, ny = x + dx, y + dy
        if (0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != "#" and
                ((nx, ny, direction) not in dist or dist[(nx, ny, direction)] > score + 1)):
            dist[(nx, ny, direction)] = score + 1
            heapq.heappush(pq, (score + 1, nx, ny, direction))

    return dist


def find_number_tiles_best_path(grid, best_score):
    start, end = parse_input(grid)
    from_start = dijkstra(grid, [(start[0], start[1], "E")])
    from_end = dijkstra(grid, [(end[0], end[1], d) for d in "EWNS"])
    flip = {"E": "W", "W": "E", "N": "S", "S": "N"}
    result = set()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            for direction in "EWNS":
                state_from_start = (row, col, direction)
                state_from_end = (row, col, flip[direction])
                if state_from_start in from_start and state_from_end in from_end:
                    if from_start[state_from_start] + from_end[state_from_end] == best_score:
                        result.add((row, col))
    return len(result)


# Example usage
if __name__ == "__main__":
    file_path = "example_1.txt"  # Replace with your file name
    maze = read_grid_from_file(file_path)
    best_score = solve_maze(maze)
    print(best_score)
    print(find_number_tiles_best_path(maze, best_score))

    file_path = "example_2.txt"  # Replace with your file name
    maze = read_grid_from_file(file_path)
    best_score = solve_maze(maze)
    print(best_score)
    print(find_number_tiles_best_path(maze, best_score))

    file_path = "input.txt"  # Replace with your file name
    maze = read_grid_from_file(file_path)
    best_score = solve_maze(maze)
    print(best_score)
    print(find_number_tiles_best_path(maze, best_score))
