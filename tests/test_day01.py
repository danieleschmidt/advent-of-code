"""Tests for Day 1 solution."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from solutions.aoc2024.day01.solution import part1, part2, parse


SAMPLE = ["3   4", "4   3", "2   5", "1   3", "3   9", "3   3"]


def test_parse():
    left, right = parse(SAMPLE)
    assert left == [3, 4, 2, 1, 3, 3]
    assert right == [4, 3, 5, 3, 9, 3]


def test_part1_sample():
    assert part1(SAMPLE) == 11


def test_part2_sample():
    assert part2(SAMPLE) == 31
