import math
from typing import Tuple, List, Optional

depth_measurements = []
while True:
    try:
        depth_measurement = int(input())
        depth_measurements.append(depth_measurement)
    except EOFError:
        break

is_part2 = True
""" How many measurements are larger than the previous measurement? """

if not is_part2:
    answer = len([m for i, m in enumerate(depth_measurements) if i > 0 and m > depth_measurements[i - 1]])
    # answer = 0
    # for i, m in enumerate(depth_measurements):
    #     if i > 0 and m > depth_measurements[i - 1]:
    #         answer += 1
else:
    """ --- Part Two ---
    Considering every single measurement isn't as useful as you expected: there's just too much noise in the data.
    Instead, consider sums of a three-measurement sliding window. Again considering the above example:
    199  A      
    200  A B    
    208  A B C  
    210    B C D
    200  E   C D
    207  E F   D
    240  E F G  
    269    F G H
    260      G H
    263        H
    Start by comparing the first and second three-measurement windows. 
    The measurements in the first window are marked A (199, 200, 208); their sum is 199 + 200 + 208 = 607. 
    The second window is marked B (200, 208, 210); its sum is 618. The sum of measurements in the second window is larger than the sum of the first, so this first comparison increased.
    
    Your goal now is to count the number of times the sum of measurements in this sliding window increases from the previous sum. 
    So, compare A with B, then compare B with C, then C with D, and so on. Stop when there aren't enough measurements left to create a new three-measurement sum.
 """
    depth_measurements = [sum(depth_measurements[i: i + 3]) for i in range(len(depth_measurements)) if i + 3 <= len(depth_measurements)]
    answer = len([m for i, m in enumerate(depth_measurements) if i > 0 and m > depth_measurements[i - 1]])
    # answer = 0
    # for i, m in enumerate(depth_measurements):
    #     if i > 0 and m > depth_measurements[i - 1]:
    #         answer += 1

print(answer)
