def list_pair_diff(lst1, lst2):
    lst1.sort()
    lst2.sort()
    return sum([abs(x - y) for x, y in zip(lst1, lst2)])


def read_columns_to_lists(filename):
    lst1 = []
    lst2 = []
    with open(filename, 'r') as file:
        for line in file:
            values = line.split()
            if len(values) == 2:
                lst1.append(int(values[0]))
                lst2.append(int(values[1]))
    return lst1, lst2


def similarity_score(lst1, lst2):
    total_sum = 0
    for num in lst1:
        if num not in lst2:
            continue
        else:
            total_sum += lst2.count(num) * num
    return total_sum


if __name__ == '__main__':
    # lst1, lst2 = read_columns_to_lists('test_input.txt')
    # print(lst1)  # Output: [1, 3, 5]
    # print(lst2)  # Output: [2, 4, 6]

    lst1, lst2 = read_columns_to_lists('input.txt')
    print(list_pair_diff(lst1, lst2))
    print(similarity_score(lst1, lst2))
