"""Tests for Day 2 solution."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from solutions.aoc2024.day02.solution import is_safe, is_safe_dampened, part1, part2


def test_is_safe_increasing():
    assert is_safe([1, 3, 6, 7, 9]) is True


def test_is_safe_decreasing():
    assert is_safe([7, 6, 4, 2, 1]) is True


def test_is_safe_unsafe():
    assert is_safe([1, 2, 7, 8, 9]) is False


def test_is_safe_no_change():
    assert is_safe([1, 1, 2, 3]) is False


def test_dampened():
    assert is_safe_dampened([1, 3, 2, 4, 5]) is True


def test_part1_sample():
    lines = ["7 6 4 2 1", "1 2 7 8 9", "9 7 6 2 1", "1 3 2 4 5", "8 6 4 4 1", "1 3 6 7 9"]
    assert part1(lines) == 2


def test_part2_sample():
    lines = ["7 6 4 2 1", "1 2 7 8 9", "9 7 6 2 1", "1 3 2 4 5", "8 6 4 4 1", "1 3 6 7 9"]
    assert part2(lines) == 4
