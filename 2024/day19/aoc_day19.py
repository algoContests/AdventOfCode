def process_file(filename):
    parts = open(filename).read().strip().split("\n\n")
    return parts[0].split(", "), [d for d in parts[1].split("\n") if d]


def can_form_design(design, patterns):
    dp = [False] * (len(design) + 1)
    dp[0] = True
    for i in range(1, len(design) + 1):
        dp[i] = any(i >= len(p) and design[i - len(p):i] == p and dp[i - len(p)] for p in patterns)
    return dp[-1]


def part_1(towel_patterns, designs):
    """ Count possible designs """
    return len([d for d in designs if can_form_design(d, towel_patterns)])


def find_all_combinations(design, patterns, start=0, memo=None):
    if memo is None: memo = {}
    if start in memo: return memo[start]
    if start >= len(design): return 1

    memo[start] = sum(find_all_combinations(design, patterns, start + len(p), memo)
                      for p in patterns
                      if start + len(p) <= len(design) and design.startswith(p, start))
    return memo[start]


def part_2(towel_patterns, designs):
    return sum(find_all_combinations(design, towel_patterns) for design in designs)


def main():
    towel_patterns, designs = process_file('input.txt')

    print(f"result aoc day 19 - p1: {part_1(towel_patterns, designs)}")
    print(f"result aoc day 19 - p2: {part_2(towel_patterns, designs)}")


if __name__ == "__main__":
    main()
