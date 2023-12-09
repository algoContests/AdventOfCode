import os
from collections import namedtuple
from time import perf_counter
from typing import List

if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    x = open(file_name, "r").read().splitlines()

    start = perf_counter()

    t, q, xx = 0, 0, 1

    y = []
    for i in range(6):
        p = ['#'] * 40
        y.append(p)

    y = ['.'] * 240
    l, ii = 0, 0

    for i in x:
        if i == 'noop':
            if ii % 40 in (xx - 1, xx, xx + 1):
                y[ii] = '#'
            ii += 1
        else:
            a, b = i.split()
            b = int(b)

            if ii % 40 in (xx - 1, xx, xx + 1):
                y[ii] = '#'
            ii += 1
            if ii % 40 in (xx - 1, xx, xx + 1):
                y[ii] = '#'

            ii += 1

            xx += b

    for i in range(6):
        print(" ".join(y[i * 40:i * 40 + 40]))

##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....

elapsed_time = (perf_counter() - start) * 1000
print(f'elapsed time = {round(elapsed_time, 2)} ms')
