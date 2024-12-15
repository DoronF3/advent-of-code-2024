def parse_input(file_path):
    """Parse the input file and return a list of machines."""
    machines = []
    with open(file_path, 'r') as f:
        while True:
            try:
                # Read button A
                line = f.readline().strip()
                if not line:
                    break

                xa_plus, ya_plus = line.split(': ')[1].split(', ')
                xa = int(xa_plus.split('+')[1])
                ya = int(ya_plus.split('+')[1])

                # Read button B
                line = f.readline().strip()
                xb_plus, yb_plus = line.split(': ')[1].split(', ')
                xb = int(xb_plus.split('+')[1])
                yb = int(yb_plus.split('+')[1])

                # Read prize location
                line = f.readline().strip()
                xp_equal, yp_equal = line.split(': ')[1].split(', ')
                xp = int(xp_equal.split('=')[1])
                yp = int(yp_equal.split('=')[1])

                # Append machine configuration
                machines.append(((xa, ya), (xb, yb), (xp, yp)))

                # Skip empty line
                f.readline()
            except Exception as e:
                print(f"Error parsing input: {e}")
                break
    return machines


def solve_claw_machine(xa, ya, xb, yb, xp, yp):
    """
    Solve the claw machine system of equations:
    xa * a + xb * b = xp
    ya * a + yb * b = yp
    Return the minimum cost if possible, otherwise return 0 if the solution is invalid.
    """
    # Calculate the determinant to check for solvability
    det = xa * yb - xb * ya
    if det == 0:
        # No unique solution (either no solution or infinitely many solutions)
        return 0

    # Calculate potential solutions for `a` and `b`
    try:
        sol_a = (xp * yb - yp * xb) / det
        sol_b = (yp * xa - xp * ya) / det
    except ZeroDivisionError:
        return 0

    # Ensure solutions are integers and non-negative
    if sol_a.is_integer() and sol_b.is_integer():
        sol_a, sol_b = int(sol_a), int(sol_b)
        if sol_a >= 0 and sol_b >= 0:
            # Calculate the cost: A costs 3 tokens, B costs 1 token
            return 3 * sol_a + sol_b

    # If solutions are not valid
    return 0


def calculate_total_cost(file_path):
    """Calculate the total minimum cost to win as many prizes as possible."""
    machines = parse_input(file_path)
    total_cost = 0
    prizes_won = 0

    for (xa, ya), (xb, yb), (xp, yp) in machines:
        cost = solve_claw_machine(xa, ya, xb, yb, xp, yp)
        if cost != 0:
            total_cost += cost
            prizes_won += 1

    return prizes_won, total_cost

def calculate_total_cost_extended(file_path):
    """Calculate the total minimum cost to win as many prizes as possible."""
    machines = parse_input(file_path)
    total_cost = 0
    prizes_won = 0

    for (xa, ya), (xb, yb), (xp, yp) in machines:
        cost = solve_claw_machine(xa, ya, xb, yb, xp+10000000000000, yp+10000000000000)
        if cost != 0:
            total_cost += cost
            prizes_won += 1

    return prizes_won, total_cost


# Example usage
if __name__ == "__main__":
    input_file = "example_1.txt"
    prizes, cost = calculate_total_cost(input_file)
    print(f"Prizes won: {prizes}, Total cost: {cost}")

    input_file = "input.txt"
    prizes, cost = calculate_total_cost(input_file)
    print(f"Prizes won: {prizes}, Total cost: {cost}")

    input_file = "example_1.txt"
    prizes, cost = calculate_total_cost_extended(input_file)
    print(f"Prizes won: {prizes}, Total cost: {cost}")

    input_file = "input.txt"
    prizes, cost = calculate_total_cost_extended(input_file)
    print(f"Prizes won: {prizes}, Total cost: {cost}")