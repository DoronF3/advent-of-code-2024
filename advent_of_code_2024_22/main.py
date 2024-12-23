import time
from collections import defaultdict
from functools import lru_cache


# Caching the results of next_secret_number using LRU Cache
@lru_cache(maxsize=None)
def next_secret_number(secret):
    # Step 1: Multiply by 64, XOR, and prune
    secret = (secret * 64) ^ secret
    secret = secret % 16777216

    # Step 2: Divide by 32, round down, XOR, and prune
    secret = (secret // 32) ^ secret
    secret = secret % 16777216

    # Step 3: Multiply by 2048, XOR, and prune
    secret = (secret * 2048) ^ secret
    secret = secret % 16777216

    return secret


def simulate_secret_numbers(initial_secrets):
    total_sum = 0

    for initial_secret in initial_secrets:
        secret = initial_secret

        # Simulate 2000 secret numbers
        for _ in range(2000):
            secret = next_secret_number(secret)

        # Add the 2000th secret number to the total sum
        total_sum += secret

    return total_sum


def get_prices(initial_secret):
    secret = initial_secret
    prices = [secret % 10]

    # Generate 2000 secret numbers and get prices
    for _ in range(2000):
        secret = next_secret_number(secret)
        prices.append(secret % 10)  # Prices are the last digit of the secret number

    return prices


def get_changes(prices):
    return [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]


def match_sequence_to_price(prices, changes):
    sequences = {}
    for i in range(len(changes) - 3):
        seq = tuple(changes[i:i + 4])
        if seq not in sequences:
            sequences[seq] = prices[i + 4]
    return sequences


def read_input_from_file(filename):
    with open(filename, 'r') as file:
        # Read lines from the file and convert them to integers
        initial_secrets = [int(line.strip()) for line in file.readlines()]
    return initial_secrets


def get_max_bananas(filename):
    initial_secrets = read_input_from_file(filename)
    score = {}
    for secret in initial_secrets:
        prices = get_prices(secret)
        changes = get_changes(prices)
        sequences = match_sequence_to_price(prices, changes)
        for sequence, price in sequences.items():
            if sequence not in score:
                score[sequence] = price
            else:
                score[sequence] += price
    return max(score.values())


# Main logic, executed only if this script is run directly
if __name__ == "__main__":
    start_time = time.time()  # Start timing the execution

    filename = 'example_1.txt'  # Replace with the path to your input file
    initial_secrets = read_input_from_file(filename)
    result = simulate_secret_numbers(initial_secrets)
    print("Total sum:", result)

    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f} seconds")

    start_time = time.time()  # Start timing the execution

    filename = 'input.txt'  # Replace with the path to your input file
    initial_secrets = read_input_from_file(filename)
    result = simulate_secret_numbers(initial_secrets)
    print("Total sum:", result)

    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f} seconds")

    start_time = time.time()  # Start timing the execution
    filename = 'example_2.txt'  # Replace with the path to your input file
    print(get_max_bananas(filename))
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f} seconds")

    start_time = time.time()  # Start timing the execution
    filename = 'input.txt'  # Replace with the path to your input file
    print(get_max_bananas(filename))
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f} seconds")
