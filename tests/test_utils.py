"""Tests for AoC utility functions."""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.aoc import (
    read_ints,
    read_grid,
    grid_neighbors,
    transpose,
    chunk,
    manhattan_distance,
    count_occurrences,
)


def test_read_ints_basic():
    assert read_ints("1 2 3") == [1, 2, 3]


def test_read_ints_negative():
    assert read_ints("-5 10 -3") == [-5, 10, -3]


def test_read_ints_mixed():
    assert read_ints("mul(3,4)") == [3, 4]


def test_read_grid():
    g = read_grid("abc\ndef")
    assert g == [["a","b","c"],["d","e","f"]]


def test_grid_neighbors_center():
    neighbors = list(grid_neighbors(1, 1, 3, 3))
    assert len(neighbors) == 4
    assert (0, 1) in neighbors
    assert (2, 1) in neighbors


def test_grid_neighbors_corner():
    neighbors = list(grid_neighbors(0, 0, 3, 3))
    assert len(neighbors) == 2


def test_grid_neighbors_diagonals():
    neighbors = list(grid_neighbors(1, 1, 3, 3, diagonals=True))
    assert len(neighbors) == 8


def test_transpose():
    g = [[1, 2], [3, 4]]
    assert transpose(g) == [[1, 3], [2, 4]]


def test_chunk():
    result = list(chunk([1, 2, 3, 4, 5], 2))
    assert result == [[1, 2], [3, 4], [5]]


def test_manhattan_distance():
    assert manhattan_distance((0, 0), (3, 4)) == 7


def test_manhattan_distance_same():
    assert manhattan_distance((2, 3), (2, 3)) == 0


def test_count_occurrences():
    counts = count_occurrences([1, 2, 1, 3, 2, 1])
    assert counts[1] == 3
    assert counts[2] == 2
    assert counts[3] == 1
