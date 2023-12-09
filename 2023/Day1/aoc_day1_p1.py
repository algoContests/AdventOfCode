with open('input.txt', 'r') as file:
    data = file.readlines()
    result: int = 0
    for input in data:
        line: list = list(input.strip())
        line = list(filter(lambda x: x.isdigit(), line))
        a, b = line[0], line[-1]
        result += int(a + b)

print(result)