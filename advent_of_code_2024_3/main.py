import re


def find_mul_expressions(file_path):
    pattern = re.compile(r'mul\((\d+),(\d+)\)')
    mul_expressions = []

    with open(file_path, 'r') as file:
        for line in file:
            matches = pattern.findall(line)
            for match in matches:
                number1, number2 = map(int, match)
                mul_expressions.append((number1, number2))

    return mul_expressions


def find_mul_do_dont_expressions(file_path):
    pattern = re.compile(r"do\(\)|don't\(\)|mul\(\d+,\d+\)")
    expressions = []

    with open(file_path, 'r') as file:
        for line in file:
            matches = pattern.findall(line)
            for match in matches:
                expressions.append(match)

    return expressions


def calc_mul_expression(expressions):
    total_sum = 0
    flag = True
    for expression in expressions:
        if expression == "do()":
            flag = True
        elif expression == "don't()":
            flag = False
        elif flag and expression.startswith("mul("):
            expression = list(map(int, expression[4:-1].split(',')))
            total_sum += expression[0] * expression[1]
    return total_sum


if __name__ == '__main__':
    file_path = 'input.txt'
    mul_expressions = find_mul_expressions(file_path)
    total_sum = 0
    for expr in mul_expressions:
        total_sum += expr[0] * expr[1]
    print(total_sum)
    expressions = find_mul_do_dont_expressions(file_path)
    print(calc_mul_expression(expressions))

