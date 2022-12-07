import os
from collections import deque


class Node:
    def __init__(self, value: str, parent=None, is_dir=True, size=0):
        self.value = value
        self.parent = parent
        self.is_dir = is_dir
        self.size = size
        self.children = []

    # def __repr__(self):
    #     return f'{self.val} {self.size}' if not self.is_dir or not self.parent else f'{self.val}/ {self.size}'

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.value) + " - " + repr(self.size) + "\n"
        for child in self.children:
            ret += child.__repr__(level+1)
        return ret

def bfs(node: Node) -> int:
    queue = deque([node])
    visited = {(node.value, node.is_dir)}
    result: int = 0
    while queue:
        parent = queue.popleft()
        for node in parent.children:
            if node.value in visited:
                continue
            if node.is_dir and node.size < 100000:
                result += node.size
            queue.append(node)
            visited.add((node.value, node.is_dir))
    print(f'{len(visited)} visited nodes')
    return result


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

        print(f'result = {bfs(root)}')
        print(f'root =\n {root}')
