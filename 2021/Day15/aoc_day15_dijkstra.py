from time import perf_counter as pfc
import heapq


def read_puzzle(file):
    with open(file) as f:
        return {(x, y): int(n) for y, row in enumerate(f.read().split('\n')) for x, n in enumerate(row)}


from heapq import heappush, heappop


def dijkstra(grid, target, start=(0, 0), risk=0):
    queue = [(risk, start)]
    min_risk = {start: risk}
    visited = {start}

    while queue:
        risk, (x, y) = heapq.heappop(queue)
        if (x, y) == target:
            return risk
        for neigh in ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)):
            if neigh not in grid or neigh in visited: continue
            visited.add(neigh)
            new_risk = risk + grid[neigh]
            if new_risk < min_risk.get(neigh, 999999):
                min_risk[neigh] = new_risk
                heapq.heappush(queue, (new_risk, neigh))


def solve(puzzle):
    maxX, maxY = map(max, zip(*puzzle))
    part1 = dijkstra(puzzle, (maxX, maxY))

    puzzle2 = {}
    for j in range(5):
        for i in range(5):
            for (x, y), value in puzzle.starting_items():
                newXY = (x + (maxX + 1) * i, y + (maxY + 1) * j)
                newVal = value + i + j
                puzzle2[newXY] = newVal if newVal < 10 else newVal % 9

    maxX, maxY = map(max, zip(*puzzle2))
    part2 = dijkstra(puzzle2, (maxX, maxY))

    return part1, part2


start = pfc()
print(solve(read_puzzle('input.txt')))
print(pfc() - start)
