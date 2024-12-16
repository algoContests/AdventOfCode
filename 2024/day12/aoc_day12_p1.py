from collections import deque

def process_file(filename: str) -> list[list[str]]:
    """
    Processes the input file into a list of lists of strings representing the map.
    """
    with open(filename) as f:
        return [list(line) for line in f.read().splitlines()]

def in_bounds(grid, x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

def part_1(grid: list) -> int:
    """Calculates the total price of fencing all regions on the map."""
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]

    def flood_fill(x, y):
        """Finds region area and perimeter."""
        plant_type = grid[x][y]
        queue, area, perimeter = deque([(x, y)]), 0, 0

        while queue:
            cx, cy = queue.popleft()
            if visited[cx][cy]:
                continue
            visited[cx][cy], area = True, area + 1

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if in_bounds(grid, nx, ny):
                    if grid[nx][ny] == plant_type and not visited[nx][ny]:
                        queue.append((nx, ny))
                    elif grid[nx][ny] != plant_type:
                        perimeter += 1
                else:
                    perimeter += 1

        return area, perimeter

    return sum(area * perimeter
               for i in range(rows)
               for j in range(cols)
               if not visited[i][j]
               for area, perimeter in [flood_fill(i, j)])

def count_sides(grid, x, y, visited, plant_type):
    """Counts the number of sides for a region."""
    sides = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        # Count edge as a side if:
        # 1. It's outside the grid
        # 2. Or it's a different plant type
        # 3. Or it's unvisited (different region of same type)
        if (not in_bounds(grid, nx, ny) or
                grid[nx][ny] != plant_type or
                not visited[nx][ny]):
            sides += 1
    return sides

def flood_fill(grid, x, y, visited):
    """Returns (area, sides) for a region."""
    if visited[x][y]:
        return 0, 0

    plant_type = grid[x][y]
    area = 0
    sides = 0
    queue = deque([(x, y)])

    while queue:
        cx, cy = queue.popleft()
        if visited[cx][cy]:
            continue

        visited[cx][cy] = True
        area += 1
        sides += count_sides(grid, cx, cy, visited, plant_type)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if (in_bounds(grid, nx, ny) and
                    not visited[nx][ny] and
                    grid[nx][ny] == plant_type):
                queue.append((nx, ny))

    return area, sides


def main() -> None:
    """
    Main function to run the program and display results for Part 1 and Part 2.
    """
    map_data = process_file('input.txt')

    print(f"result aoc day 12 - p1: {part_1(map_data)}")

if __name__ == "__main__":
    main()
