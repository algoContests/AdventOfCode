import heapq


def get_neighbors(node, graph):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    results = []
    for direction in directions:
        neighbor = (node[0] + direction[0], node[1] + direction[1])
        if neighbor in graph:
            results.append(neighbor)
    return results


def manhattan_distance(start, end):
    x1, y1 = start
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)


def find_lowest_risk(graph, start, end):
    frontier = []
    heapq.heappush(frontier, (0, start))
    risk_so_far = dict()
    risk_so_far[start] = 0

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == end:
            break

        for neighbor in get_neighbors(current, graph):
            new_risk = risk_so_far[current] + graph[neighbor]
            if neighbor not in risk_so_far or new_risk < risk_so_far[neighbor]:
                risk_so_far[neighbor] = new_risk
                priority = new_risk + manhattan_distance(neighbor, end)
                heapq.heappush(frontier, (priority, neighbor))

    return risk_so_far[end]


def main():
    with open("input.txt", 'r') as infile:
        graph = {(x, y): int(cost) for y, line in enumerate(infile.readlines()) for x, cost in enumerate(line.strip())}

    start = (0, 0)
    end = (max(x for x, y in graph.keys()), max(y for x, y in graph.keys()))

    lowest_risk = find_lowest_risk(graph, start, end)
    print(lowest_risk)


if __name__ == '__main__':
    main()
