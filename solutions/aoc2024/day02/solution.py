"""AoC 2024 Day 2: Red-Nosed Reports."""
from utils.aoc import read_lines, read_ints


def is_safe(levels: list[int]) -> bool:
    """A report is safe if strictly increasing or decreasing by 1-3."""
    diffs = [levels[i+1] - levels[i] for i in range(len(levels)-1)]
    if all(1 <= d <= 3 for d in diffs):
        return True
    if all(-3 <= d <= -1 for d in diffs):
        return True
    return False


def is_safe_dampened(levels: list[int]) -> bool:
    """Safe with Problem Dampener: tolerate removing one level."""
    if is_safe(levels):
        return True
    for i in range(len(levels)):
        candidate = levels[:i] + levels[i+1:]
        if is_safe(candidate):
            return True
    return False


def part1(lines: list[str]) -> int:
    return sum(1 for line in lines if line and is_safe(read_ints(line)))


def part2(lines: list[str]) -> int:
    return sum(1 for line in lines if line and is_safe_dampened(read_ints(line)))


if __name__ == "__main__":
    from utils.aoc import read_lines as rl
    lines = rl(2024, 2)
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))
