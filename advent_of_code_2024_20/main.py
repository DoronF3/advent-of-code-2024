from collections import deque
import time

# Directions for moving in the grid (up, down, left, right)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def parse_input(input_file):
    """Parses the grid to extract start, end, walls, and dimensions."""
    start, end, walls = None, None, set()
    with open(input_file, 'r') as file:
        grid = [line.strip() for line in file]

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'S':
                start = (x, y)
            elif cell == 'E':
                end = (x, y)
            elif cell == '#':
                walls.add((x, y))

    return len(grid), len(grid[0]), start, end, walls


def bfs_distance_map(rows, cols, start, walls):
    """Performs BFS and returns a distance map."""
    queue = deque([start])
    distances = {start: 0}

    while queue:
        x, y = queue.popleft()
        for dx, dy in DIRECTIONS:
            neighbor = (x + dx, y + dy)
            if (0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows and
                    neighbor not in walls and neighbor not in distances):
                distances[neighbor] = distances[(x, y)] + 1
                queue.append(neighbor)
    return distances


def find_all_shortest_paths(rows, cols, start, end, walls, shortest_path):
    """Finds all cheat scenarios where bypassing walls saves steps."""
    start_distances = bfs_distance_map(rows, cols, start, walls)
    end_distances = bfs_distance_map(rows, cols, end, walls)
    cheat_scenarios = {}

    for x, y in walls:
        for dx, dy in DIRECTIONS:
            n1, n2 = (x + dx, y + dy), (x - dx, y - dy)
            if n1 in start_distances and n2 in end_distances:
                path_length = start_distances[n1] + 1 + end_distances[n2]
                time_saved = shortest_path - path_length
                if time_saved > 0:
                    cheat_scenarios[time_saved] = cheat_scenarios.get(time_saved, 0) + 1

    return cheat_scenarios


def count_cheats_threshold(cheat_scenarios, threshold):
    """Counts cheat scenarios exceeding a given time threshold."""
    return sum(count for time_saved, count in cheat_scenarios.items() if time_saved >= threshold)


def manhattan(x1, y1, x2, y2):
    """Calculate the Manhattan distance between two points."""
    return abs(x1 - x2) + abs(y1 - y2)


def simulate_cheat(distance_map, time_threshold):
    count = 0
    # Iterate through all pairs of nodes (start_node, start_distance) and (end_node, end_distance)
    for start_node, start_distance in reversed(distance_map.items()):
        for end_node, end_distance in distance_map.items():
            # Calculate the Manhattan distance between the start and end nodes
            manhattan_distance = manhattan(start_node[0], start_node[1], end_node[0], end_node[1])

            # Check if the Manhattan distance is small enough and the "time saved" (shortcut) is significant
            time_saved = end_distance - start_distance - manhattan_distance
            if manhattan_distance <= 20 and time_saved >= time_threshold:
                count += 1

    return count



def process_file(filename, threshold):
    """Processes a single file and prints results."""
    start_time = time.time()
    rows, cols, start, end, walls = parse_input(filename)
    distances = bfs_distance_map(rows, cols, start, walls)
    cheat_scenarios = find_all_shortest_paths(rows, cols, start, end, walls, distances.get(end, float('inf')))
    print(f"Processing '{filename}'")
    print(count_cheats_threshold(cheat_scenarios, threshold)) # example_1.txt: 5
    if filename == 'example_1.txt':
        print(simulate_cheat(distances, 72)) # Should be 29
    else:
        print(simulate_cheat(distances, 100))
    print(f'Time: {time.time() - start_time:.4f} seconds')


if __name__ == "__main__":
    total_start_time = time.time()

    process_file('example_1.txt', 20)
    process_file('input.txt', 100)
