import re
from functools import lru_cache


def process_file(filename):
    with open(filename) as f:
        data = f.read()
    return ([int(x) for x in re.findall(r'Register \w: (\d+)', data)],
            tuple(int(x) for x in re.search(r'Program: ([\d,]+)', data).group(1).split(',')))


@lru_cache(maxsize=None)
def execute_program(registers, program, ip=0):
    """
    Exécute le programme de manière récursive avec mémoïsation.
    'registers', 'program', et 'ip' doivent être immuables (tuples) pour être cachables.
    """
    if ip >= len(program):
        return []

    # Copie mutable pour modification
    A, B, C = list(registers)

    opcode = program[ip]
    operand = program[ip + 1]
    next_ip = ip + 2

    def get_combo_value(op):
        return op if op <= 3 else (A if op == 4 else (B if op == 5 else C))

    output_segment = []
    if opcode == 0: A //= 2 ** get_combo_value(operand)
    elif opcode == 1: B ^= operand
    elif opcode == 2: B = get_combo_value(operand) % 8
    elif opcode == 3:
        if A != 0: next_ip = operand
    elif opcode == 4: B ^= C
    elif opcode == 5: output_segment.append(get_combo_value(operand) % 8)
    elif opcode == 6: B = A // (2 ** get_combo_value(operand))
    elif opcode == 7: C = A // (2 ** get_combo_value(operand))
    else: raise ValueError(f"Unknown opcode: {opcode}")

    # Appel récursif pour la suite de l'exécution
    new_registers = (A, B, C)
    return output_segment + execute_program(new_registers, program, next_ip)


def part_1(registers, program):
    # Cette fonction n'est plus le cœur de la solution, mais on la garde pour la forme.
    # La logique principale est maintenant dans part_2.
    return "Utilisez part_2 pour la solution."


def part_2(registers, program, max_a=20000000):
    """
    Trouve la plus petite valeur de 'a' qui produit la séquence de sortie attendue.
    Utilise un interpréteur itératif avec détection de cycle pour être efficace.
    """
    target_output = list(program)

    for a_val in range(1, max_a + 1):
        # Initialise les registres pour cet essai
        A, B, C = a_val, registers[1], registers[2]
        ip = 0
        output = []

        # Dictionnaire pour détecter les cycles. Clé: (A, B, C, ip), Valeur: longueur de la sortie à cet état.
        history = {}

        while ip < len(program):
            state = (A, B, C, ip)
            if state in history:
                # Cycle détecté !
                prev_len = history[state]
                cycle_len = len(output) - prev_len
                cycle_pattern = output[prev_len:]

                # Vérifie si le motif du cycle correspond à la séquence cible
                remaining_len = len(target_output) - len(output)
                if remaining_len > 0:
                    # Prolonge la sortie avec le motif du cycle pour correspondre à la longueur cible
                    num_repeats = (remaining_len + cycle_len - 1) // cycle_len
                    output.extend((cycle_pattern * num_repeats)[:remaining_len])
                break  # Sort de la simulation, on a la sortie complète

            history[state] = len(output)

            opcode = program[ip]
            operand = program[ip + 1]
            next_ip = ip + 2

            def get_combo_value(op):
                return op if op <= 3 else (A if op == 4 else (B if op == 5 else C))

            if opcode == 0: A //= 2 ** get_combo_value(operand)
            elif opcode == 1: B ^= operand
            elif opcode == 2: B = get_combo_value(operand) % 8
            elif opcode == 3:
                if A != 0: next_ip = operand
            elif opcode == 4: B ^= C
            elif opcode == 5:
                val = get_combo_value(operand) % 8
                output.append(val)
                # Arrêt anticipé si la sortie diverge
                if len(output) > len(target_output) or output[-1] != target_output[len(output)-1]:
                    break
            elif opcode == 6: B = A // (2 ** get_combo_value(operand))
            elif opcode == 7: C = A // (2 ** get_combo_value(operand))
            else: raise ValueError(f"Unknown opcode: {opcode}")

            ip = next_ip

        if output == target_output:
            return a_val

    raise ValueError(f"Aucune solution trouvée jusqu'à {max_a}")


def main() -> None:
    registers, program = process_file('input.txt')
    # On ne lance que la partie 2 qui est le but final
    print(f"result aoc day 17 - p2: {part_2(registers, program)}")


if __name__ == "__main__":
    main()
