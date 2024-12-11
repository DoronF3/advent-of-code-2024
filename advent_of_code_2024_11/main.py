import time
from collections import defaultdict


def load_input(filename):
    """Load grid data from a file into a 2D list."""
    with open(filename, 'r') as file:
        return [int(num) for line in file for num in line.split()]


# Helper function to perform the blink operation
def blink(stones):
    new_stones = defaultdict(int)
    for number, count in stones.items():
        if number == 0:
            new_stones[1] += count
        elif len(str(number)) % 2 == 0:
            # Split the number into two parts
            num_str = str(number)
            left = int(num_str[:len(num_str) >> 1])
            right = int(num_str[len(num_str) >> 1:])
            new_stones[left] += count
            new_stones[right] += count
        else:
            # Multiply the number by 2024
            new_stones[(number << 11) - (number << 3) - (number << 4)] += count
    return new_stones


# Function to simulate the stones' evolution for a given number of blinks
def simulate_blinks(initial_stones, blinks):
    stones = defaultdict(int)

    # Initializing the stones dictionary with the input values
    for stone in initial_stones:
        stones[stone] += 1

    # Perform blinks
    for _ in range(blinks):
        stones = blink(stones)

    # Return the total number of stones
    return sum(stones.values())


def time_function(func, *args):
    """Decorator to time a function call."""
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    print(f"Execution time of {func.__name__}: {end_time - start_time:.6f} seconds")
    return result


if __name__ == '__main__':
    line = load_input('example_1.txt')
    print(time_function(simulate_blinks, line, 25))

    line = load_input('input.txt')
    print(time_function(simulate_blinks, line, 25))

    line = load_input('input.txt')
    print(time_function(simulate_blinks, line, 75))
