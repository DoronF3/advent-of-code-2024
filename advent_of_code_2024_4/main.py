def find_all_occurrences(grid, target):
    def count_word_in_direction(x, y, dx, dy):
        for i in range(len(target)):  # Check if the word matches in the given direction
            nx, ny = x + i * dx, y + i * dy
            if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
                return 0  # Out of bounds
            if grid[nx][ny] != target[i]:
                return 0  # Doesn't match the word
        return 1  # Found a match

    def count_from_cell(x, y):
        directions = [  # (dx, dy) pairs for 8 directions
            (0, 1),  # right
            (1, 0),  # down
            (0, -1),  # left
            (-1, 0),  # up
            (1, 1),  # down-right diagonal
            (-1, -1),  # up-left diagonal
            (1, -1),  # down-left diagonal
            (-1, 1)  # up-right diagonal
        ]
        total = 0
        for dx, dy in directions:  # Check each direction
            total += count_word_in_direction(x, y, dx, dy)
        return total

    count = 0
    for x in range(len(grid)):  # Iterate over each cell in the grid
        for y in range(len(grid[0])):
            count += count_from_cell(x, y)

    return count


def load_grid_from_file(filename):
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            grid.append(list(line.strip()))  # Convert each line to a list of characters
    return grid


def find_xmas_patterns(grid):
    def is_valid_xmas(x, y):
        """
        Check all possible configurations of the X-MAS pattern centered at (x, y).
        """
        center = grid[x][y] == 'A'  # The center must always be 'A'
        if not center:
            return False

        # Define all possible "X-MAS" configurations
        patterns = [
            [(x - 1, y - 1, 'M'), (x - 1, y + 1, 'M'), (x + 1, y - 1, 'S'), (x + 1, y + 1, 'S')],  # Top M bottom S
            [(x - 1, y - 1, 'S'), (x - 1, y + 1, 'S'), (x + 1, y - 1, 'M'), (x + 1, y + 1, 'M')],  # Top S bottom M
            # Reverse diagonals: bottom-left to top-right
            [(x + 1, y - 1, 'M'), (x - 1, y - 1, 'M'), (x + 1, y + 1, 'S'), (x - 1, y + 1, 'S')],  # Left M right S
            [(x + 1, y - 1, 'S'), (x - 1, y - 1, 'S'), (x + 1, y + 1, 'M'), (x - 1, y + 1, 'M')],  # Left S right M
        ]

        # Check if any of these patterns match
        for pattern in patterns:
            if all(
                    0 <= px < len(grid) and 0 <= py < len(grid[0]) and grid[px][py] == value
                    for px, py, value in pattern
            ):
                return True
        return False

    count = 0
    for x in range(len(grid)):  # Iterate over each cell in the grid
        for y in range(len(grid[0])):
            if is_valid_xmas(x, y):
                count += 1
    return count


if __name__ == '__main__':
    grid = [
        ['.', '.', 'X', '.', '.', '.'],
        ['.', 'S', 'A', 'M', 'X', '.'],
        ['.', 'A', '.', '.', 'A', '.'],
        ['X', 'M', 'A', 'S', '.', 'S'],
        ['.', 'X', '.', '.', '.', '.']
    ]

    target_word = "XMAS"
    occurrences = find_all_occurrences(grid, target_word)
    print(f"Number of occurrences of '{target_word}':", occurrences)

    example_path = 'example_input.txt'
    grid = load_grid_from_file(example_path)
    target_word = "XMAS"
    occurrences = find_all_occurrences(grid, target_word)
    print(f"Number of occurrences of '{target_word}':", occurrences)

    file_path = 'input.txt'
    grid = load_grid_from_file(file_path)
    occurrences = find_all_occurrences(grid, target_word)
    print(f"Number of occurrences of '{target_word}':", occurrences)

    # Example usage
    grid = [
        ['.', 'M', '.', 'S', '.', '.', '.', '.', '.', '.'],
        ['.', '.', 'A', '.', '.', 'M', 'S', 'M', 'S', '.'],
        ['.', 'M', '.', 'S', '.', 'M', 'A', 'A', '.', '.'],
        ['.', '.', 'A', '.', 'A', 'S', 'M', 'S', 'M', '.'],
        ['.', 'M', '.', 'S', '.', 'M', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['S', '.', 'S', '.', 'S', '.', 'S', '.', 'S', '.'],
        ['.', 'A', '.', 'A', '.', 'A', '.', 'A', '.', '.'],
        ['M', '.', 'M', '.', 'M', '.', 'M', '.', 'M', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ]

    occurrences = find_xmas_patterns(grid)
    print(f"Number of X-MAS patterns:", occurrences)

    file_path = 'input.txt'
    grid = load_grid_from_file(file_path)
    occurrences = find_xmas_patterns(grid)
    print(f"Number of X-MAS patterns:", occurrences)