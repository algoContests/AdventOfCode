#
#   Day 1: find the two entries that sum to 2020 and then multiply those two numbers together.
#

def find_2_entries(tab):
    for i in tab:
        for j in tab:
            if i + j == 2020:
                return i * j

def find_3_entries(tab):
    for i in tab:
        for j in tab:
            for k in tab:
                if i + j + k == 2020:
                    return i * j * k

expense_report = list(map(int, input().split()))

print(find_2_entries(expense_report))
print(find_3_entries(expense_report))
