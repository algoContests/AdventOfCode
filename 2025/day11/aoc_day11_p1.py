from collections import deque

def process_file(filename: str) -> dict:
	with open(filename) as f:
		graph = dict()
		for line in f:
			node, edges_list = line.strip().split(":")
			edge_list = [e.strip() for e in edges_list.split() if e]
			if node in graph:
				graph[node] += edge_list
			else:
				graph[node] = edge_list
		return graph


def part_1(graph: dict) -> int:
	queue = deque([('you', [])])
	paths = []
	while queue:
		node, path = queue.popleft()
		if node == 'out':
			paths.append(path)
			continue
		for new_node in graph[node]:
			new_path = path + [new_node]
			queue.append((new_node, new_path))
	return len(paths)



def main() -> None:
	graph = process_file('input.txt')
	print(f"result aoc day 11 - p1: {part_1(graph)}")


if __name__ == "__main__":
	main()
