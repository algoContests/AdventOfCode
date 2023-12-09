line = input()
yes_response = {}
persons_count = 0
# groups_count = 0
yes_count = 0
while True:
    try:
        if line == '':
            yes_count += len([key for key, value in yes_response.items() if value == persons_count])
            yes_response = {}
            persons_count = 0
            # groups_count += 1
        else:
            persons_count += 1
            for car in list(line):
                if car in yes_response:
                    yes_response[car] += 1
                else:
                    yes_response[car] = 1
        line = input()
    except EOFError:
        yes_count += len([key for key, value in yes_response.items() if value == persons_count])
        break

# print(f'{groups_count} groups')
print(yes_count)
