def parse_input(file_path):
    with open(file_path, 'r') as file:
        data = []
        for line in file:
            result, values = line.split(':')
            result = int(result.strip())
            values = list(map(int, values.split()))
            data.append((result, values))
    return data


def check_equation(data):
    correct_sum = 0
    for equation in data:
        if helper(equation[0], equation[1], 1, equation[1][0]):
            correct_sum += equation[0]
    return correct_sum


def helper(result, values, index, current_sum):
    if index == len(values):
        return result == current_sum
    return (helper(result, values, index + 1, current_sum + values[index]) or
            helper(result, values, index + 1, current_sum * values[index]))


def check_equation_2(data):
    correct_sum = 0
    for equation in data:
        if helper_2(equation[0], equation[1], 1, equation[1][0]):
            correct_sum += equation[0]
    return correct_sum


def helper_2(result, values, index, current_sum):
    if index == len(values):
        return result == current_sum
    return (helper_2(result, values, index + 1, current_sum + values[index]) or
            helper_2(result, values, index + 1, current_sum * values[index]) or
            helper_2(result, values, index + 1, int(str(current_sum) + str(values[index]))))


if __name__ == '__main__':
    data = parse_input('example_1.txt')
    print(check_equation(data))

    data = parse_input('input.txt')
    print(check_equation(data))

    data = parse_input('example_1.txt')
    print(check_equation_2(data))

    data = parse_input('input.txt')
    print(check_equation_2(data))
