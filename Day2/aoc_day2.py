#
#   Day 2:How many passwords are valid according to their policies?
#

def is_valid_first(i):
    policy, password = map(str, i.split(':'))
    letter_range, letter = map(str, policy.split())
    min, max = map(int, letter_range.split('-'))
    count_letter = len([l for l in password if l == letter])
    return int(min) <= count_letter <= int(max)

def is_valid_second(i):
    policy, password = map(str, i.split(':'))
    p = password.lstrip()
    letter_range, letter = map(str, policy.split())
    first, second = map(int, letter_range.split('-'))
    letters = [l for idx, l in enumerate(p) if l == letter and idx + 1 in {first, second}]
    return True if len(letters) == 1 else False

valid_pass_1 = valid_pass_2 = 0
# 1-14 b: bbbbbbbbbbbbbbbbbbb
for _ in range(1000):
    i = input()
    valid_pass_1 += 1 if is_valid_first(i) else 0
    valid_pass_2 += 1 if is_valid_second(i) else 0

print(valid_pass_1)
print(valid_pass_2)

