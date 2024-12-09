def load_grid_from_file(filename):
    """Load grid data from a file into a 2D list."""
    with open(filename, 'r') as file:
        return [list(line.strip()) for line in file]


def find_antennas(grid):
    """
    Identify antennas in the grid and group their positions by label.

    Returns:
        dict: Keys are antenna labels, values are lists of positions (tuples).
    """
    antennas = {}
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell != ".":
                antennas.setdefault(cell, []).append((i, j))
    return antennas


def create_following_tuples_dict(antennas):
    """
    Create a mapping from each antenna position to subsequent positions.

    Returns:
        dict: Keys are positions, values are lists of following positions.
    """
    return {positions[i]: positions[i + 1:]
            for key, positions in antennas.items()
            for i in range(len(positions) - 1)}


def calculate_antinodes(grid, antennas):
    """
    Calculate unique antinodes based on antennas and their positions.

    Returns:
        int: Count of unique antinodes.
    """
    antinodes = set()
    rows, cols = len(grid), len(grid[0])

    for antenna, positions in antennas.items():
        for pos in positions:
            dx, dy = antenna[0] - pos[0], antenna[1] - pos[1]
            antinode_1 = (antenna[0] + dx, antenna[1] + dy)
            antinode_2 = (pos[0] - dx, pos[1] - dy)

            # Add antinodes if they are within grid boundaries
            if 0 <= antinode_1[0] < rows and 0 <= antinode_1[1] < cols:
                antinodes.add(antinode_1)
            if 0 <= antinode_2[0] < rows and 0 <= antinode_2[1] < cols:
                antinodes.add(antinode_2)

    return len(antinodes)


def calculate_antinodes_extended(grid, antennas):
    """
    Calculate extended unique antinodes based on antennas and positions.

    Returns:
        int: Count of unique extended antinodes.
    """
    antinodes = set()
    rows, cols = len(grid), len(grid[0])

    for antenna, positions in antennas.items():
        for pos in positions:
            dx, dy = antenna[0] - pos[0], antenna[1] - pos[1]
            i, flag = 0, False

            while not flag:
                flag = True
                antinode_1 = (antenna[0] + dx * i, antenna[1] + dy * i)
                antinode_2 = (pos[0] - dx * i, pos[1] - dy * i)

                # Add antinodes if they are within grid boundaries
                if 0 <= antinode_1[0] < rows and 0 <= antinode_1[1] < cols:
                    antinodes.add(antinode_1)
                    flag = False
                if 0 <= antinode_2[0] < rows and 0 <= antinode_2[1] < cols:
                    antinodes.add(antinode_2)
                    flag = False
                i += 1

    return len(antinodes)


def process_file(filename, extended=False):
    """
    Process the grid file and calculate antinodes.

    Args:
        filename (str): The file path.
        extended (bool): Whether to calculate extended antinodes.

    Returns:
        int: Count of antinodes.
    """
    grid = load_grid_from_file(filename)
    antennas = find_antennas(grid)
    antennas_to_check = create_following_tuples_dict(antennas)

    if extended:
        return calculate_antinodes_extended(grid, antennas_to_check)
    return calculate_antinodes(grid, antennas_to_check)


if __name__ == '__main__':
    files = ['example_1.txt', 'input.txt', 'example_2.txt']
    for file in files:
        print(f"File: {file}, Antinodes: {process_file(file)}")
        print(f"File: {file}, Extended Antinodes: {process_file(file, extended=True)}")
