
yes_count = 0
yes_response = {}
while True:
    try:
        line = input()
        if len(list(line)) == 0:
            yes_count += len(yes_response)
            yes_response = {}
        else:
            for car in list(line):
                yes_response[car] = 1
    except:
        yes_count += len(yes_response)
        break

print(yes_count)
