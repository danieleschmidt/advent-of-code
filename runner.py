#!/usr/bin/env python3
"""Run AoC solution for a given year and day."""
import sys
import importlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def run(year: int, day: int) -> None:
    module_path = f"solutions.{year}.day{day:02d}.solution"
    try:
        mod = importlib.import_module(module_path)
    except ModuleNotFoundError:
        print(f"No solution found for {year} day {day}")
        sys.exit(1)

    input_file = Path(__file__).parent / "solutions" / str(year) / f"day{day:02d}" / "input.txt"
    if not input_file.exists():
        print(f"Missing input file: {input_file}")
        sys.exit(1)

    text = input_file.read_text().strip()
    lines = text.splitlines()

    if hasattr(mod, "part1"):
        print(f"Part 1: {mod.part1(lines if mod.part1.__code__.co_varnames[0] == 'lines' else text)}")
    if hasattr(mod, "part2"):
        print(f"Part 2: {mod.part2(lines if mod.part2.__code__.co_varnames[0] == 'lines' else text)}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python runner.py <year> <day>")
        sys.exit(1)
    run(int(sys.argv[1]), int(sys.argv[2]))
