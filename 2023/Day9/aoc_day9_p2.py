import sys, re

from typing import List


def debug(*args):
    # return
    print(*args, file=sys.stderr)
    sys.stderr.flush()

if __name__ == "__main__":
    with open('input.txt') as f:
        data = f.read().strip()

    histories = []
    for line in data.split('\n'):
        # histories.append(re.findall(r"(\d)", line))
        histories.append(list(map(int, line.split())))

    predictions = []
    for h in histories:
        # print('------START_------')
        seq = [*h]
        sequences:  List[List[int]] = []
        sequences.append(seq)
        while not all(map(lambda x: x == 0, seq)):
            seq = [seq[i] - seq[i-1] for i in range(1, len(seq))]
            sequences.append(seq)
        # for s in sequences:
        #     print(s)
        result: int = 0
        for i in range(len(sequences) - 1, -1, -1):
            result = sequences[i][0] - result
        predictions.append(result)

    print(predictions) # 18, 28, 68
    print(sum(predictions)) # 114
