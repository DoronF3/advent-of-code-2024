def parse_schematics(file_path):
    def process_schematic(schematic, is_lock):
        """Process the schematic grid into heights."""
        if schematic:
            (locks if is_lock else keys).append(get_heights(schematic, is_lock))

    locks, keys = [], []
    current_schematic = []
    is_lock = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                process_schematic(current_schematic, is_lock)
                current_schematic = []
                continue

            if not current_schematic:
                is_lock = line.startswith('#')
            current_schematic.append(line)

    process_schematic(current_schematic, is_lock)
    return locks, keys


def get_heights(grid, lock=True):
    def calculate_height(col_range):
        """Calculate the height for a column range."""
        heights = []
        for col in col_range:
            height = 0
            for row in (range(len(grid)) if lock else reversed(range(len(grid)))):
                if grid[row][col] == '#':
                    height += 1
                else:
                    break
            heights.append(height - 1)
        return heights

    return calculate_height(range(len(grid[0])))


def fits(lock, key, rows):
    """Check if the lock and key fit within the row constraints."""
    return all(lock[i] + key[i] <= rows - 1 for i in range(len(lock)))


def count_valid_pairs(locks, keys, rows):
    """Count valid lock and key pairs."""
    return sum(fits(lock, key, rows) for lock in locks for key in keys)


if __name__ == '__main__':
    for file_path in ['example_1.txt', 'input.txt']:
        locks, keys = parse_schematics(file_path)
        rows = 6  # Number of rows in the schematics
        result = count_valid_pairs(locks, keys, rows)
        print(f"Valid lock/key pairs in {file_path}:", result)
