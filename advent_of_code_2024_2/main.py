def is_increasing(lst):
    return all(1 <= lst[i] - lst[i - 1] <= 3 for i in range(1, len(lst)))


def is_almost_increasing(lst):
    for i in range(1, len(lst)):
        if not (1 <= lst[i] - lst[i - 1] <= 3):
            return is_increasing(lst[:i] + lst[i + 1:]) or is_increasing(lst[:i - 1] + lst[i:])

    return True


if __name__ == '__main__':
    safe_list_count = 0
    safe_list_count_with_one_bad = 0
    with open('input.txt', 'r') as file:
        for line in file:
            numbers = list(map(int, line.split()))
            if numbers[-1] < numbers[0]:
                numbers.reverse()
            if is_increasing(numbers):
                safe_list_count += 1
            if is_almost_increasing(numbers):
                safe_list_count_with_one_bad += 1
    print(safe_list_count)  # Output the count of safe lists
    print(safe_list_count_with_one_bad)  # Output the count of safe lists with one bad element
