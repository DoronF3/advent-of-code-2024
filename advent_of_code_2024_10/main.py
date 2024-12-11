def load_grid_from_file(filename):
    """Load grid data from a file into a 2D list."""
    with open(filename, 'r') as file:
        return [list(map(int, line.strip())) for line in file if line.strip()]


def get_trail_heads(grid):
    """Identify all trailheads (positions with height 0) in the grid."""
    return [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 0]


def explore_trails(grid, x, y, visited_nines):
    """
    DFS to find all unique height-9 positions reachable from (x, y).
    Only track visited `9` positions.
    """
    if not (0 <= x < len(grid) and 0 <= y < len(grid[0])):
        return 0

    current_height = grid[x][y]

    # If we've reached a 9, add it to visited_nines and stop exploring further
    if current_height == 9 and (x, y) not in visited_nines:
        if (x, y) not in visited_nines:
            visited_nines.add((x, y))
            return 1
        return 0

    # Explore all neighbors that are one step higher
    reachable_nines = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == current_height + 1:
            reachable_nines += explore_trails(grid, nx, ny, visited_nines)

    return reachable_nines


def sum_trails(grid, trail_heads):
    """Calculate the sum of scores for all trailheads."""
    total_score = 0
    for trail_head in trail_heads:
        visited_nines = set()  # Track only visited `9` positions
        total_score += explore_trails(grid, trail_head[0], trail_head[1], visited_nines)
    return total_score


def explore_trails_ratings(grid, x, y):
    """
    DFS to find all unique height-9 positions reachable from (x, y).
    Only track visited `9` positions.
    """
    if not (0 <= x < len(grid) and 0 <= y < len(grid[0])):
        return 0

    current_height = grid[x][y]

    # If we've reached a 9, add it to visited_nines and stop exploring further
    if current_height == 9:
        return 1

    # Explore all neighbors that are one step higher
    reachable_nines = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == current_height + 1:
            reachable_nines += explore_trails_ratings(grid, nx, ny)

    return reachable_nines


def sum_trails_ratings(grid, trail_heads):
    """Calculate the sum of scores for all trailheads."""
    total_score = 0
    for trail_head in trail_heads:
        total_score += explore_trails_ratings(grid, trail_head[0], trail_head[1])
    return total_score


if __name__ == '__main__':
    grid = load_grid_from_file('example_1.txt')
    trail_heads = get_trail_heads(grid)
    print(sum_trails(grid, trail_heads))

    grid = load_grid_from_file('example_2.txt')
    trail_heads = get_trail_heads(grid)
    print(sum_trails(grid, trail_heads))

    grid = load_grid_from_file('input.txt')
    trail_heads = get_trail_heads(grid)
    print(sum_trails(grid, trail_heads))

    grid = load_grid_from_file('example_1.txt')
    trail_heads = get_trail_heads(grid)
    print(sum_trails_ratings(grid, trail_heads))

    grid = load_grid_from_file('example_2.txt')
    trail_heads = get_trail_heads(grid)
    print(sum_trails_ratings(grid, trail_heads))

    grid = load_grid_from_file('input.txt')
    trail_heads = get_trail_heads(grid)
    print(sum_trails_ratings(grid, trail_heads))
