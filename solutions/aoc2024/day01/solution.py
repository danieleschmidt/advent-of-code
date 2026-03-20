"""AoC 2024 Day 1: Historian Hysteria."""
from utils.aoc import read_lines, read_ints


def parse(lines: list[str]) -> tuple[list[int], list[int]]:
    left, right = [], []
    for line in lines:
        nums = read_ints(line)
        if len(nums) >= 2:
            left.append(nums[0])
            right.append(nums[1])
    return left, right


def part1(lines: list[str]) -> int:
    """Total distance between sorted lists."""
    left, right = parse(lines)
    return sum(abs(a - b) for a, b in zip(sorted(left), sorted(right)))


def part2(lines: list[str]) -> int:
    """Similarity score: sum of left * count in right."""
    left, right = parse(lines)
    counts = {}
    for n in right:
        counts[n] = counts.get(n, 0) + 1
    return sum(n * counts.get(n, 0) for n in left)


if __name__ == "__main__":
    from utils.aoc import read_lines as rl
    lines = rl(2024, 1)
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))
