def get_adjacent_octopus_positions(x, y):
    adjacent_octopus_positions = []
    for dx in range(-1, 2, 1):
        for dy in range(-1, 2, 1):
            if (dx, dy) != (0, 0):
                n_x, n_y = x + dx, y + dy
                if 0 <= n_x < 10 and 0 <= n_y < 10:
                    adjacent_octopus_positions.append((n_x, n_y))
    return adjacent_octopus_positions

print(get_adjacent_octopus_positions(1, 1))
