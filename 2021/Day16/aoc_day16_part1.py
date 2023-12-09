from collections import deque


class SinglePacket:
    version: int
    a: int
    b: int
    c: int

    def __init__(self, version: int):
        self.version = version


file = 'input_example.txt'
with open(file) as f:
    binary_msg = bin(int(f.read(), 16))[2:]

""" 
    Every packet begins with a standard header: the first three bits encode the packet version, and the next three bits encode the packet type ID.
"""
print(binary_msg)

""" Packets with type ID 4 represent a literal value. Literal value packets encode a single binary number.
        The three bits labeled V (110) are the packet version, 6.
        The three bits labeled T (100) are the packet type ID, 4, which means the packet is a literal value.
        The five bits labeled A (10111) start with a 1 (not the last group, keep reading) and contain the first four bits of the number, 0111.
        The five bits labeled B (11110) start with a 1 (not the last group, keep reading) and contain four more bits of the number, 1110.
        The five bits labeled C (00101) start with a 0 (last group, end of packet) and contain the last four bits of the number, 0101.
        The three unlabeled 0 bits at the end are extra due to the hexadecimal representation and should be ignored.
"""
""" Every other type of packet (any packet with a type ID other than 4) represent an operator that performs some calculation on one or more sub-packets contained within.
"""
packet_start, packet_end = True, False
packet_group = ''

if packet_start:
    i = 0
    while not int(binary_msg[i]):
        i += 1
    version = f'0b{binary_msg[i: i + 3]}'
    version = int(version, 2)
    type_id = f'0b{binary_msg[i + 3: i + 6]}'
    type_id = int(type_id, 2)
    if type_id == 4:
        i += 6
        packet_group = ""
        while not packet_end:
            last_group = not int(binary_msg[i])
            if last_group:
                pack_end = True
            i += 1
            packet_group += binary_msg[i: i + 4]
            i += 4

print(packet_group)
