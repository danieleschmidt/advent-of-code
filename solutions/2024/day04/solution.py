"""AoC 2024 Day 4: Ceres Search — find XMAS in word search."""
from utils.aoc import read_lines, read_grid


def part1(lines: list[str]) -> int:
    """Count occurrences of XMAS in all 8 directions."""
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0]) if grid else 0
    word = "XMAS"
    count = 0
    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for r in range(rows):
        for c in range(cols):
            for dr, dc in dirs:
                if all(
                    0 <= r+i*dr < rows and 0 <= c+i*dc < cols
                    and grid[r+i*dr][c+i*dc] == word[i]
                    for i in range(len(word))
                ):
                    count += 1
    return count


def part2(lines: list[str]) -> int:
    """Count X-MAS: two MAS in an X shape."""
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0]) if grid else 0
    count = 0
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if grid[r][c] != "A":
                continue
            diag1 = grid[r-1][c-1] + grid[r][c] + grid[r+1][c+1]
            diag2 = grid[r-1][c+1] + grid[r][c] + grid[r+1][c-1]
            if diag1 in ("MAS", "SAM") and diag2 in ("MAS", "SAM"):
                count += 1
    return count


if __name__ == "__main__":
    from utils.aoc import read_lines as rl
    lines = rl(2024, 4)
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))
