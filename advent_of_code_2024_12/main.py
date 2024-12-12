def load_grid_from_file(filename):
    """Load grid data from a file into a 2D list."""
    with open(filename, 'r') as file:
        return [list(line.strip()) for line in file]


def calculate_fencing_cost(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]

    def is_valid(r, c, plant_type):
        return 0 <= r < rows and 0 <= c < cols and not visited[r][c] and grid[r][c] == plant_type

    def flood_fill(r, c, plant_type):
        stack = [(r, c)]
        visited[r][c] = True
        area = 0
        perimeter = 0

        while stack:
            x, y = stack.pop()
            area += 1
            # Check each direction
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny, plant_type):
                    stack.append((nx, ny))
                    visited[nx][ny] = True
                elif not (0 <= nx < rows and 0 <= ny < cols) or grid[nx][ny] != plant_type:
                    # Increment perimeter if out of bounds or adjacent to a different plant
                    perimeter += 1

        return area, perimeter

    total_cost = 0

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                plant_type = grid[r][c]
                area, perimeter = flood_fill(r, c, plant_type)
                total_cost += area * perimeter

    return total_cost


def flood_fill_extended(grid, x, y, visited, plant_type):
    stack = [(x, y)]  # Track cells to visit
    region_cells = set()
    rows, cols = len(grid), len(grid[0])

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))
        region_cells.add((cx, cy))

        # Check neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] == plant_type and (nx, ny) not in visited:
                    stack.append((nx, ny))
    return region_cells


def calculate_sides(region_cells):
    count = 0
    for pos in region_cells:

        left = (pos[0], pos[1] - 1) in region_cells
        right = (pos[0], pos[1] + 1) in region_cells
        up = (pos[0] - 1, pos[1]) in region_cells
        down = (pos[0] + 1, pos[1]) in region_cells
        up_left = (pos[0] - 1, pos[1] - 1) in region_cells
        up_right = (pos[0] - 1, pos[1] + 1) in region_cells
        down_left = (pos[0] + 1, pos[1] - 1) in region_cells
        down_right = (pos[0] + 1, pos[1] + 1) in region_cells

        if not left and not up:
            count += 1
        if not right and not up:
            count += 1
        if not left and not down:
            count += 1
        if not right and not down:
            count += 1
        if not up_right and up and right:
            count += 1
        if not up_left and up and left:
            count += 1
        if not down_left and down and left:
            count += 1
        if not down_right and down and right:
            count += 1

    return count


def calculate_total_price(grid):
    visited = set()
    total_price = 0

    rows, cols = len(grid), len(grid[0])

    for x in range(rows):
        for y in range(cols):
            if (x, y) not in visited:
                plant_type = grid[x][y]
                region_cells = flood_fill_extended(grid, x, y, visited, plant_type)
                sides = calculate_sides(region_cells)
                total_price += len(region_cells) * sides

    return total_price


if __name__ == '__main__':
    grid = load_grid_from_file('example_1.txt')
    print(calculate_fencing_cost(grid))

    grid = load_grid_from_file('example_2.txt')
    print(calculate_fencing_cost(grid))

    grid = load_grid_from_file('example_3.txt')
    print(calculate_fencing_cost(grid))

    grid = load_grid_from_file('input.txt')
    print(calculate_fencing_cost(grid))

    grid = load_grid_from_file('example_1.txt')
    print(calculate_total_price(grid))

    grid = load_grid_from_file('example_2.txt')
    print(calculate_total_price(grid))

    grid = load_grid_from_file('example_4.txt')
    print(calculate_total_price(grid))

    grid = load_grid_from_file('example_5.txt')
    print(calculate_total_price(grid))

    grid = load_grid_from_file('input.txt')
    print(calculate_total_price(grid))
