"""Tests for Day 3 solution."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from solutions.aoc2024.day03.solution import part1, part2


def test_part1_sample():
    text = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    assert part1(text) == 161


def test_part2_sample():
    text = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    assert part2(text) == 48
