def count_adjacent_rolls(grid, row, col):
    """Count the number of adjacent rolls (@) to the given position."""
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    # Check all 8 adjacent positions
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the center position

            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                count += 1

    return count


def solve(input_file='input.txt'):
    """Solve Part 1: count initially accessible rolls."""
    with open(input_file, 'r') as f:
        grid = [line.strip() for line in f]

    accessible_count = 0

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '@':
                adjacent = count_adjacent_rolls(grid, row, col)
                if adjacent < 4:
                    accessible_count += 1

    return accessible_count


def solve_part2(input_file='input.txt'):
    """Solve Part 2: count total rolls that can be removed iteratively."""
    with open(input_file, 'r') as f:
        grid = [list(line.strip()) for line in f]  # Mutable grid

    total_removed = 0

    while True:
        # Find all accessible rolls in current state
        accessible = []
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == '@':
                    adjacent = count_adjacent_rolls(grid, row, col)
                    if adjacent < 4:
                        accessible.append((row, col))

        if not accessible:
            break  # No more accessible rolls

        # Remove all accessible rolls
        for row, col in accessible:
            grid[row][col] = '.'

        total_removed += len(accessible)

    return total_removed


def main():
    result1 = solve()
    print(f"Part 1 - Number of accessible rolls: {result1}")

    result2 = solve_part2()
    print(f"Part 2 - Total rolls that can be removed: {result2}")


if __name__ == "__main__":
    main()
