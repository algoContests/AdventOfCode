import math
from typing import Tuple, List, Optional


def find_row(p: str):
    """ The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0 through 127).
        Each letter tells you which half of a region the given seat is in.
        Start with the whole list of rows; the first letter indicates whether the seat is in the front (0 through 63) or the back (64 through 127).
        The next letter indicates which half of that region the seat is in, and so on until you're left with exactly one row.For example, consider just the first seven characters of FBFBBFFRLR:
            Start by considering the whole range, rows 0 through 127.
            F means to take the lower half, keeping rows 0 through 63.
            B means to take the upper half, keeping rows 32 through 63.
            F means to take the lower half, keeping rows 32 through 47.
            B means to take the upper half, keeping rows 40 through 47.
            B keeps rows 44 through 47.
            F keeps rows 44 through 45.
            The final F keeps the lower of the two, row 44.
    """
    n_rows = 2 ** 7
    a, b = 0, n_rows - 1
    for c in p:
        n_rows //= 2
        if not n_rows:
            break
        if c == 'F':
            b = a + n_rows - 1
        else:
            a = b - n_rows + 1
    return a


def find_col(p: str):
    """ The last three characters will be either L or R; these specify exactly one of the 8 columns of seats on the plane (numbered 0 through 7).
        The same process as above proceeds again, this time with only three steps. L means to keep the lower half, while R means to keep the upper half.

        For example, consider just the last 3 characters of FBFBBFFRLR:

        Start by considering the whole range, columns 0 through 7.
        R means to take the upper half, keeping columns 4 through 7.
        L means to take the lower half, keeping columns 4 through 5.
        The final R keeps the upper of the two, column 5.
    """
    n_cols = 2 ** 3
    a, b = 0, n_cols - 1
    for c in p:
        n_cols //= 2
        if not n_cols:
            break
        if c == 'L':
            b = a + n_cols - 1
        else:
            a = b - n_cols + 1
    return b


""" Here are some other boarding passes:
    FBFBBFFRLR: row 44, column 5, seat ID 357
    BFFFBBFRRR: row 70, column 7, seat ID 567.
    FFFBBBFRRR: row 14, column 7, seat ID 119.
    BBFFBBFRLL: row 102, column 4, seat ID 820.
"""

liste = ['FBFBBFFRLR', 'BFFFBBFRRR', 'FFFBBBFRRR', 'BBFFBBFRLL']

for encoded_seat_number in liste:
    row, col = find_row(p=encoded_seat_number[:-3]), find_col(p=encoded_seat_number[-3:])
    seat_id = row * 8 + col
    print(f'row {row}, column {col}, seat ID {seat_id}')

max_seat_id = -math.inf
existing_seats = []
while True:
    try:
        encoded_seat_number = input()
        row, col = find_row(p=encoded_seat_number[:-3]), find_col(p=encoded_seat_number[-3:])
        seat_id = row * 8 + col
        existing_seats.append(seat_id)
        if seat_id > max_seat_id:
            max_seat_id = seat_id
    except EOFError:
        print(max_seat_id)
        break

""" --- Part Two ---
    Ding! The "fasten seat belt" signs have turned on. Time to find your seat.
    It's a completely full flight, so your seat should be the only missing boarding pass in your list. 
    However, there's a catch: some of the seats at the very front and back of the plane don't exist on this aircraft, so they'll be missing from your list as well.
    Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours will be in your list.
    
    What is the ID of your seat?
"""
diff = 2**8 - max_seat_id # 1024 - 816 = 208
# full_list = list(range(diff - 1, 2**8 - diff + 1))
full_list = range(207, 1024 - 208 + 1)

for seat_id in full_list:
    if seat_id not in existing_seats:
        print(seat_id)
        break
