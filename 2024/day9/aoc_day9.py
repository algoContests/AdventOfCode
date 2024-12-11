from itertools import chain

import numpy as np


def process_file(filename: str) -> str:
    """
    Processes the input file into a string representing the disk layout.
    """
    with open(filename) as f:
        return f.read().strip()


def compact_disk_map_v1(disk_map):
    blocks = []
    i = 0

    while i < len(disk_map):
        if i % 2 == 0:
            file_id, file_length = str(i // 2), int(disk_map[i])
            blocks.extend([file_id] * file_length)
        else:
            free_blocks = int(disk_map[i])
            blocks.extend(['.'] * free_blocks)
        i += 1

    while True:
        try:
            free_block_idx = blocks.index('.')
            blocks[free_block_idx] = blocks[-1]
            blocks.pop()
        except ValueError:
            break
    return blocks


def compact_disk_map_v2_short(disk_map):
    blocks = []
    for i in range(len(disk_map)):
        blocks.extend([str(i // 2) if i % 2 == 0 else '.'] * int(disk_map[i]))

    files = {b: {'start': i, 'size': blocks[i:].count(b)}
             for i, b in enumerate(blocks) if b != '.' and blocks.index(b) == i}

    for file_id in sorted(files.keys(), key=int, reverse=True):
        file = files[file_id]
        for i in range(file['start']):
            if all(b == '.' for b in blocks[i:i + file['size']]):
                blocks[file['start']:file['start'] + file['size']] = ['.'] * file['size']
                blocks[i:i + file['size']] = [file_id] * file['size']
                break

    return blocks


def compact_disk_map_v2(disk_map):
    # Convert to numpy array for faster operations
    blocks = np.array(list(chain.from_iterable(
        [str(i // 2)] * int(n) if i % 2 == 0 else ['.'] * int(n)
        for i, n in enumerate(disk_map)
    )))

    # Use numpy operations for faster processing
    unique_files = np.unique(blocks[blocks != '.'])
    for file_id in sorted(unique_files, key=int, reverse=True):
        mask = blocks == file_id
        size = np.sum(mask)
        start = np.where(mask)[0][0]

        # Find free space using numpy operations
        dots = blocks == '.'
        kernel = np.ones(size)
        conv = np.convolve(dots, kernel, mode='valid')

        # Find leftmost position where file fits
        valid_positions = np.where(conv == size)[0]
        if len(valid_positions) > 0 and valid_positions[0] < start:
            new_pos = valid_positions[0]
            blocks[start:start + size] = '.'
            blocks[new_pos:new_pos + size] = file_id

    return blocks.tolist()


def compact_disk_map_v2_ori(disk_map):
    blocks = []
    i = 0

    while i < len(disk_map):
        if i % 2 == 0:
            file_id, file_length = i // 2, int(disk_map[i])
            blocks.extend([file_id] * file_length)
        else:
            free_blocks = int(disk_map[i])
            blocks.extend(['.'] * free_blocks)
        i += 1

    file_positions = {}
    for index, block in enumerate(blocks):
        if block != '.':
            if block not in file_positions:
                file_positions[block] = []
            file_positions[block].append(index)

    for file_id in sorted(file_positions.keys(), reverse=True):
        file_blocks = file_positions[file_id]
        if not file_blocks:
            continue
        start = min(file_blocks)
        end = max(file_blocks)
        file_length = end - start + 1

        move_to = None
        for i in range(start):
            if blocks[i] == '.' and all(block == '.' for block in blocks[i:i + file_length]):
                move_to = i
                break

        if move_to is not None:
            for i in range(file_length):
                blocks[start + i] = '.'
                blocks[move_to + i] = file_id

    return blocks


def calculate_checksum(compacted_blocks):
    checksum = 0
    for position, block in enumerate(compacted_blocks):
        if block != '.':
            checksum += position * int(block)
    return checksum


def part_1(disk_map: str) -> int:
    compacted_blocks = compact_disk_map_v1(disk_map)
    return calculate_checksum(compacted_blocks)


def part_2(disk_map: str) -> int:
    compacted_blocks = compact_disk_map_v2(disk_map)
    return calculate_checksum(compacted_blocks)


def main() -> None:
    """
    Main function to run the program and display results for Part 1 and Part 2.
    """
    disk_map = process_file('input.txt')

    # print(f"result aoc day 9 - p1: {part_1(disk_map)}")
    print(f"result aoc day 9 - p2: {part_2(disk_map)}")


if __name__ == "__main__":
    main()
