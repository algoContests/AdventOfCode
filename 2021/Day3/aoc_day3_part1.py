""" --- Day 3: Binary Diagnostic --- Part 1 """

binary_numbers = []
while True:
    try:
        binary_number = map(int, input())
        binary_numbers.append(binary_number)
    except EOFError:
        break

w = 12
d = [{0: 0, 1: 0} for _ in range(w)]
for binary_number in binary_numbers:
    for i, digit in enumerate(list(binary_number)):
        if digit == 0:
            d[i][0] += 1
        else:
            d[i][1] += 1

gamma, epsilon = [], []
for i, d in enumerate(d):
    gamma.append(max(d.items(), key=lambda x: x[1])[0])
    epsilon.append(min(d.items(), key=lambda x: x[1])[0])

gamma = ''.join(map(str, gamma))
epsilon = ''.join(map(str, epsilon))
gamma = int(gamma, 2)
epsilon = int(epsilon, 2)
power_consumption = gamma * epsilon

print(power_consumption)
