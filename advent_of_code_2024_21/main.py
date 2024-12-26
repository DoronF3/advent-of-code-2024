import time
from collections import defaultdict
from functools import reduce

# Define the pads as static dictionaries
numeric_pad = {
    "7": (0, 0), "8": (0, 1), "9": (0, 2),
    "4": (1, 0), "5": (1, 1), "6": (1, 2),
    "1": (2, 0), "2": (2, 1), "3": (2, 2),
    "0": (3, 1), "A": (3, 2), "gap": (3, 0)
}

dir_pad = {

    "gap": (0, 0), "^": (0, 1), "A": (0, 2),
    "<": (1, 0), "v": (1, 1), ">": (1, 2)

}


def parse_input(input_file):
    with open(input_file) as f:
        return f.read().strip().split("\n")


def shortest_path(key1, key2, pad):
    x1, y1 = pad[key1]
    x2, y2 = pad[key2]

    ud, lr = ["v"] * (x2 - x1) if x2 > x1 else ["^"] * (x1 - x2), [">"] * (y2 - y1) if y2 > y1 else ["<"] * (y1 - y2)

    if y2 > y1 and (x2, y1) != pad["gap"]:
        move = ud + lr + ['A']
    elif (x1, y2) != pad["gap"]:
        move = lr + ud + ['A']
    else:
        move = ud + lr + ['A']

    return move


def sequences(seq, pad):
    keys = []
    prev_key = "A"
    for key in seq:
        keys += shortest_path(prev_key, key, pad)
        prev_key = key
    return keys


def calculate_shortest_seq_len(codes):
    # Cache is handled by lru_cache
    r1_seqs = [sequences(code, numeric_pad) for code in codes]
    r2_seqs = [sequences(seq, dir_pad) for seq in r1_seqs]
    r3_seqs = [sequences(seq, dir_pad) for seq in r2_seqs]

    return sum(len(seq) * int(code[:-1]) for seq, code in zip(r3_seqs, codes))


def shortest_path_2(key1, key2, pad):
    x1, y1 = pad[key1]
    x2, y2 = pad[key2]

    ud, lr = "v" * (x2 - x1) if x2 > x1 else "^" * (x1 - x2), ">" * (y2 - y1) if y2 > y1 else "<" * (y1 - y2)

    if y2 > y1 and (x2, y1) != pad["gap"]:
        return f"{ud}{lr}A"
    if (x1, y2) != pad["gap"]:
        return f"{lr}{ud}A"
    return f"{ud}{lr}A"


def sequences_2(seq, pad):
    keys = []
    prev_key = "A"
    for key in seq:
        keys.append(shortest_path_2(prev_key, key, pad))
        prev_key = key
    return keys


def seq_counts(seq):
    # Generate frequency table of sub-sequences
    freq_table = defaultdict(int)
    seq_2 = sequences_2(seq, dir_pad)
    for s in seq_2:
        freq_table[s] += 1
    return freq_table


def complexity(codes, num_dir_robots=25):
    # Initialize frequency tables
    f_tables = [defaultdict(int, {''.join(sequences_2(code, numeric_pad)): 1}) for code in codes]

    # Expand sequences for each robot iteration
    def expand_sequences(f_tables):
        new_f_tables = []
        for f_table in f_tables:
            sub_f_table = defaultdict(int)
            for seq, freq in f_table.items():
                for sub_seq, sub_freq in seq_counts(seq).items():
                    sub_f_table[sub_seq] += sub_freq * freq
            new_f_tables.append(sub_f_table)
        return new_f_tables

    f_tables = reduce(lambda tables, _: expand_sequences(tables), range(num_dir_robots), f_tables)

    # Calculate the final complexity
    def calculate_complexity(seq):
        return sum(len(key) * freq for key, freq in seq.items())

    return sum(calculate_complexity(seq) * int(code[:-1]) for seq, code in zip(f_tables, codes))


if __name__ == "__main__":
    start_time = time.time()
    file = "example_1.txt"
    codes = parse_input(file)
    print(calculate_shortest_seq_len(codes))

    end_time = time.time()
    print(f"Execution Time: {end_time - start_time:.4f} seconds")

    start_time = time.time()
    file = "input.txt"
    codes = parse_input(file)
    print(calculate_shortest_seq_len(codes))
    end_time = time.time()
    print(f"Execution Time: {end_time - start_time:.4f} seconds")

    start_time = time.time()
    file = "input.txt"
    codes = parse_input(file)
    print(complexity(codes))
    end_time = time.time()
    print(f"Execution Time: {end_time - start_time:.4f} seconds")
