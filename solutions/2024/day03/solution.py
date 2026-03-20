"""AoC 2024 Day 3: Mull It Over."""
import re
from utils.aoc import read_input


def part1(text: str) -> int:
    """Sum all mul(X,Y) instructions."""
    return sum(int(a) * int(b) for a, b in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", text))


def part2(text: str) -> int:
    """Sum mul(X,Y) only when enabled (do()/don't())."""
    total = 0
    enabled = True
    for token in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)", text):
        match = token.group()
        if match == "do()":
            enabled = True
        elif match == "don't()":
            enabled = False
        elif enabled:
            total += int(token.group(1)) * int(token.group(2))
    return total


if __name__ == "__main__":
    from utils.aoc import read_input as ri
    text = ri(2024, 3)
    print("Part 1:", part1(text))
    print("Part 2:", part2(text))
