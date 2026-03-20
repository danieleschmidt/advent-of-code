"""AoC 2024 Day 5: Print Queue."""
from utils.aoc import read_input
from functools import cmp_to_key


def parse(text: str):
    sections = text.strip().split("\n\n")
    rules_text, updates_text = sections[0], sections[1]
    rules = set()
    for line in rules_text.splitlines():
        a, b = line.split("|")
        rules.add((int(a), int(b)))
    updates = []
    for line in updates_text.splitlines():
        updates.append([int(x) for x in line.split(",")])
    return rules, updates


def is_valid(update: list[int], rules: set) -> bool:
    for i in range(len(update)):
        for j in range(i + 1, len(update)):
            if (update[j], update[i]) in rules:
                return False
    return True


def sort_update(update: list[int], rules: set) -> list[int]:
    def cmp(a, b):
        if (a, b) in rules:
            return -1
        if (b, a) in rules:
            return 1
        return 0
    return sorted(update, key=cmp_to_key(cmp))


def part1(text: str) -> int:
    rules, updates = parse(text)
    total = 0
    for update in updates:
        if is_valid(update, rules):
            total += update[len(update) // 2]
    return total


def part2(text: str) -> int:
    rules, updates = parse(text)
    total = 0
    for update in updates:
        if not is_valid(update, rules):
            fixed = sort_update(update, rules)
            total += fixed[len(fixed) // 2]
    return total


if __name__ == "__main__":
    from utils.aoc import read_input as ri
    text = ri(2024, 5)
    print("Part 1:", part1(text))
    print("Part 2:", part2(text))
