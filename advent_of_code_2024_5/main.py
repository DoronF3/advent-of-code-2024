def parse_input(input_str):
    with open(input_str) as f:
        input_str = f.read()
        # Split into rules and updates
        rules_section, updates_section = input_str.strip().split("\n\n")
        # Parse rules
        rules = [tuple(map(int, line.split("|"))) for line in rules_section.splitlines()]
        # Parse updates
        updates = [list(map(int, line.split(","))) for line in updates_section.splitlines()]
    return rules, updates


def is_update_valid(update, rules):
    # Create a lookup for the order of pages in this update
    page_order = {page: idx for idx, page in enumerate(update)}
    return all(page_order[A] < page_order[B] for A, B in rules)


def reorganize(update, rules):
    # Build the graph and calculate in-degrees
    # Start with the pages in a random order (initially, the given order)
    sorted_update = update[:]
    changed = True

    while changed:
        changed = False
        for A, B in rules:
            # Ensure A comes before B
            index_A = sorted_update.index(A)
            index_B = sorted_update.index(B)
            if index_A > index_B:
                # Swap A and B to satisfy the rule
                sorted_update.remove(A)
                sorted_update.insert(index_B, A)
                changed = True

    return sorted_update


def calculate_middle_sum(input_str):
    # Parse the input
    rules, updates = parse_input(input_str)
    middle_sum = 0
    incorrect_sum = 0
    for update in updates:
        # Filter relevant rules
        relevant_rules = [(A, B) for A, B in rules if A in update and B in update]
        if is_update_valid(update, relevant_rules):
            # Calculate the middle page
            middle_page = update[len(update) // 2]
            middle_sum += middle_page
        else:
            fixed = reorganize(update, relevant_rules)
            middle_page = fixed[len(fixed) // 2]
            incorrect_sum += middle_page
    return middle_sum, incorrect_sum


if __name__ == '__main__':
    print(calculate_middle_sum('example_1.txt'))

    print(calculate_middle_sum('input.txt'))
