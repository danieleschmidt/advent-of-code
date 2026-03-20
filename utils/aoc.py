"""Shared Advent of Code utilities."""
from __future__ import annotations
import re
from pathlib import Path
from typing import Iterator


def read_input(year: int, day: int) -> str:
    """Read puzzle input for a given year/day."""
    path = Path(__file__).parent.parent / "solutions" / str(year) / f"day{day:02d}" / "input.txt"
    return path.read_text().strip()


def read_lines(year: int, day: int) -> list[str]:
    """Read puzzle input as a list of lines."""
    return read_input(year, day).splitlines()


def read_ints(text: str) -> list[int]:
    """Extract all integers from a string."""
    return [int(x) for x in re.findall(r"-?\d+", text)]


def read_grid(text: str) -> list[list[str]]:
    """Parse text as a 2D grid of characters."""
    return [list(line) for line in text.splitlines()]


def grid_neighbors(r: int, c: int, rows: int, cols: int, diagonals: bool = False) -> Iterator[tuple[int, int]]:
    """Yield valid (row, col) neighbors for a grid cell."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if diagonals:
        directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc


def transpose(grid: list[list]) -> list[list]:
    """Transpose a 2D list."""
    return [list(row) for row in zip(*grid)]


def chunk(lst: list, size: int) -> Iterator[list]:
    """Split list into chunks of given size."""
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    """Manhattan distance between two (row, col) points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def count_occurrences(items: list) -> dict:
    """Count occurrences of each item."""
    counts: dict = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts
