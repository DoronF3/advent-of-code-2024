import time


def parse_input(file_path):
    """Parse input from a file and generate the disk map."""
    with open(file_path, 'r') as file:
        line = file.read()
        disk_map = list(map(int, line.rstrip()))

    new_map = []
    current_id = 0
    for idx, val in enumerate(disk_map):
        # Append file ID or free space based on index parity
        new_map.extend([current_id if idx % 2 == 0 else '.'] * val)
        if idx % 2 == 0:
            current_id += 1
    return new_map


def compact(data):
    result = data[:]
    data_rev = data[::-1]
    i = result.index('.')
    j = 0
    while len(data) - j > i:
        if data_rev[j] != '.':
            result[i] = data_rev[j]
            result[len(data) - j - 1] = '.'
            i = result.index('.')
        j += 1
    return result


def identify_files(data):
    """Identify files and their lengths in the input data."""
    files = []
    current_file = None
    start_index = None

    for i, ch in enumerate(data):
        if ch != '.':
            if current_file != ch:
                if current_file is not None:
                    files.append((current_file, start_index, i - start_index))
                current_file = ch
                start_index = i
        elif current_file is not None:
            files.append((current_file, start_index, i - start_index))
            current_file = None
            start_index = None

    if current_file is not None:  # Add the last file
        files.append((current_file, start_index, len(data) - start_index))

    return files


def identify_free_spaces(data):
    """Identify contiguous free spaces in the input data."""
    free_spaces = []
    start = None

    for i, ch in enumerate(data):
        if ch == '.':
            if start is None:
                start = i
        elif start is not None:
            free_spaces.append((start, i - start))
            start = None

    if start is not None:  # Add the last free space
        free_spaces.append((start, len(data) - start))

    return free_spaces


def merge_free_spaces(free_spaces):
    """Merge adjacent or overlapping free spaces."""
    merged = []
    for start, length in sorted(free_spaces, key=lambda x: x[0]):
        if merged and merged[-1][0] + merged[-1][1] >= start:
            prev_start, prev_length = merged.pop()
            merged.append((prev_start, max(prev_start + prev_length, start + length) - prev_start))
        else:
            merged.append((start, length))
    return merged


def compact_extended(data):
    result = data[:]  # Create a copy of the input data to avoid modifying the original

    # Step 1: Identify files and free spaces
    files = identify_files(data)
    free_spaces = identify_free_spaces(data)

    # Step 2: Move files in descending order of file ID
    for file_id, start_idx, file_length in sorted(files, key=lambda x: -int(x[0])):
        for idx, (free_start, free_length) in enumerate(free_spaces):
            if free_length >= file_length and free_start < start_idx:
                # Move the file
                result[free_start:free_start + file_length] = result[start_idx:start_idx + file_length]
                result[start_idx:start_idx + file_length] = ['.'] * file_length

                # Update free spaces
                free_spaces[idx] = (free_start + file_length, free_length - file_length)
                if free_spaces[idx][1] == 0:
                    free_spaces.pop(idx)

                free_spaces.append((start_idx, file_length))
                free_spaces = merge_free_spaces(free_spaces)
                break

    return result


def calculate_checksum(data):
    """Calculate the checksum for the disk map."""
    return sum(idx * val for idx, val in enumerate(data) if val != '.')


def time_function(func, *args):
    """Decorator to time a function call."""
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    print(f"Execution time of {func.__name__}: {end_time - start_time:.6f} seconds")
    return result


if __name__ == '__main__':
    # Time each of the operations
    print("Processing example_1.txt")
    data = parse_input('example_1.txt')
    compact_data = time_function(compact, data)
    print(f"Checksum: {calculate_checksum(compact_data)}")

    print("\nProcessing example_2.txt")
    data = parse_input('example_2.txt')
    compact_data = time_function(compact, data)
    print(f"Checksum: {calculate_checksum(compact_data)}")

    print("\nProcessing input.txt")
    data = parse_input('input.txt')
    compact_data = time_function(compact, data)
    print(f"Checksum: {calculate_checksum(compact_data)}")

    print("\nProcessing example_1.txt with extended compaction")
    data = parse_input('example_1.txt')
    compact_data = time_function(compact_extended, data)
    print(f"Checksum: {calculate_checksum(compact_data)}")

    print("\nProcessing example_2.txt with extended compaction")
    data = parse_input('example_2.txt')
    compact_data = time_function(compact_extended, data)
    print(f"Checksum: {calculate_checksum(compact_data)}")

    print("\nProcessing input.txt with extended compaction")
    data = parse_input('input.txt')
    compact_data = time_function(compact_extended, data)
    print(f"Checksum: {calculate_checksum(compact_data)}")
