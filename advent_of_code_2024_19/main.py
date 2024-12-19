def count_possible_designs(towel_patterns, desired_designs):
    possible_count = 0

    for design in desired_designs:
        n = len(design)
        dp = [False] * (n + 1)
        dp[0] = True  # Base case: empty design can always be formed

        for i in range(1, n + 1):
            for pattern in towel_patterns:
                if i >= len(pattern) and design[i - len(pattern):i] == pattern:
                    dp[i] = dp[i] or dp[i - len(pattern)]

        if dp[n]:
            possible_count += 1

    return possible_count


# Read input from a file
def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().strip().split("\n")
        towel_patterns = lines[0].split(", ")
        desired_designs = lines[2:]  # Skip the blank line and get the designs
    return towel_patterns, desired_designs


def count_all_arrangements(towel_patterns, desired_designs):
    total_ways = 0

    for design in desired_designs:
        n = len(design)
        dp = [0] * (n + 1)
        dp[0] = 1  # Base case: one way to form an empty design

        for i in range(1, n + 1):
            for pattern in towel_patterns:
                if i >= len(pattern) and design[i - len(pattern):i] == pattern:
                    dp[i] += dp[i - len(pattern)]

        total_ways += dp[n]

    return total_ways

# Main function
if __name__ == "__main__":
    input_file = "example_1.txt"  # Specify the input file
    towel_patterns, desired_designs = read_input(input_file)
    result = count_possible_designs(towel_patterns, desired_designs)
    print(f"Number of possible designs: {result}")

    input_file = "input.txt"  # Specify the input file
    towel_patterns, desired_designs = read_input(input_file)
    result = count_possible_designs(towel_patterns, desired_designs)
    print(f"Number of possible designs: {result}")

    input_file = "example_1.txt"  # Specify the input file
    towel_patterns, desired_designs = read_input(input_file)
    result = count_all_arrangements(towel_patterns, desired_designs)
    print(f"Total number of arrangements: {result}")

    input_file = "input.txt"  # Specify the input file
    towel_patterns, desired_designs = read_input(input_file)
    result = count_all_arrangements(towel_patterns, desired_designs)
    print(f"Total number of arrangements: {result}")
