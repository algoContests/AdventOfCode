import os
from collections import deque
from typing import List


class Node:
    def __init__(self, value: str, parent=None, is_dir=True, size=0):
        self.value = value
        self.parent = parent
        self.is_dir = is_dir
        self.size = size
        self.children = []

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.value) + " - " + repr(self.size) + "\n"
        for child in self.children:
            ret += child.__repr__(level+1)
        return ret

def bfs2(node: Node, space_to_free: int) -> List[Node]:
    queue = deque([node])
    visited = {(node.value, node.is_dir)}
    candidates: List[Node] = []
    while queue:
        parent = queue.popleft()
        for node in parent.children:
            if node.value in visited:
                continue
            if node.is_dir and node.size >= space_to_free:
                candidates.append(node)
            queue.append(node)
            visited.add((node.value, node.is_dir))
    print(f'{len(visited)} visited nodes')
    return candidates


if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    with open(file_name) as file:
        root = Node(value='/')
        for line in file:
            if line[0] == '$' and line.split()[1] == 'cd':
                cmd, dir = line.split()[1:]
                if dir == '/':
                    node = root
                elif dir == '..':
                    node = node.parent
                else:
                    node = [n for n in node.children if n.is_dir and n.value == dir][0]
            elif line.split()[1] != 'ls':
                a, b = line.split()
                if a == 'dir':
                    node.children.append(Node(value=b, parent=node))
                else:
                    node.children.append(Node(value=b, parent=node, is_dir=False, size=int(a)))
                    parent = node
                    while parent:
                        parent.size += int(a)
                        parent = parent.parent

        unused_space: int = 70_000_000 - root.size
        space_to_delete: int = 30_000_000 - unused_space
        print(f'unused space = {unused_space}')
        print(f'space to free = {space_to_delete}')

        nodes_candidates: List[Node] = bfs2(root, space_to_delete)
        result: int = min([node.size for node in nodes_candidates])

        print(result)
        # print(f'root =\n {root}')
