from typing import Tuple, List, Optional

passports = []
passport = {}

# for _ in range(959):
#     line = input()
#     print(line)
#
# exit(0)


while True:
    try:
        line = input()
        if len(list(line)) == 0:
            passports.append(passport)
            passport = {}
        else:
            for item in line.split():
                key, value = item.split(':')
                passport[key] = value
    except EOFError:
        passports.append(passport)
        break

valid_keys = list(passports[0].keys())
print(valid_keys)

is_part2 = True

valid_passports_count = 0
for passport in passports:
    is_valid = True
    """ Part 1 """
    for key in valid_keys:
        if key not in passport:
            is_valid = False
    if is_part2:
        """ Part 2
            byr (Birth Year) - four digits; at least 1920 and at most 2002.
            iyr (Issue Year) - four digits; at least 2010 and at most 2020.
            eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
            hgt (Height) - a number followed by either cm or in:
            If cm, the number must be at least 150 and at most 193.
            If in, the number must be at least 59 and at most 76.
            hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
            ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
            pid (Passport ID) - a nine-digit number, including leading zeroes.
            cid (Country ID) - ignored, missing or not.
        """
        for key, value in passport.items():
            value: str
            if key == 'byr':
                if not (value.isdigit() and 1920 <= int(value) <= 2002):
                    is_valid = False
            elif key == 'iyr':
                if not (value.isdigit() and 2010 <= int(value) <= 2020):
                    is_valid = False
            elif key == 'eyr':
                if not (value.isdigit() and 2020 <= int(value) <= 2030):
                    is_valid = False
            elif key == 'hgt':
                size, unit = value[:-2], value[-2:]
                if not size.isdigit():
                    is_valid = False
                else:
                    if not (unit == 'cm' and 150 <= int(size) <= 193) and not (unit == 'in' and 59 <= int(size) <= 76):
                        is_valid = False
            elif key == 'hcl':
                if not (value[0] == '#' and len(value[1:]) == 6 and value[1:].isalnum()):
                    is_valid = False
            elif key == 'ecl':
                colors = "amb blu brn gry grn hzl oth".split()
                if value not in colors:
                    is_valid = False
            elif key == 'pid':
                if not (len(value) == 9 and value.isdigit()):
                    is_valid = False

    if is_valid:
        valid_passports_count += 1

print(valid_passports_count)
