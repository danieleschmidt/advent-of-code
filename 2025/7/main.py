from collections import deque

def find_start(grid):
    """Find the starting position 'S' in the grid."""
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'S':
                return (row, col)
    return None


def simulate_beams(grid):
    """Simulate the tachyon beams and count how many times they split."""
    start = find_start(grid)
    if not start:
        return 0

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Queue of active beams: (row, col)
    # Beams always move downward
    beams = deque([start])

    # Track which positions have been visited to avoid re-processing
    visited = set()

    split_count = 0

    while beams:
        row, col = beams.popleft()

        # Skip if we've already processed a beam at this position
        if (row, col) in visited:
            continue

        visited.add((row, col))

        # Try to move down
        next_row = row + 1

        # Check if we exit the manifold
        if next_row >= rows:
            continue

        # Check what's at the next position
        next_char = grid[next_row][col]

        if next_char == '.':
            # Continue moving down
            beams.append((next_row, col))
        elif next_char == '^':
            # Split! The beam stops, and two new beams start from left and right
            split_count += 1

            # Left beam
            left_col = col - 1
            if left_col >= 0:
                beams.append((next_row, left_col))

            # Right beam
            right_col = col + 1
            if right_col < cols:
                beams.append((next_row, right_col))
        elif next_char == 'S':
            # Treat S as empty space
            beams.append((next_row, col))

    return split_count


def simulate_quantum_particle(grid):
    """Simulate quantum particle and count unique timelines using path counting."""
    start = find_start(grid)
    if not start:
        return 0

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Count paths to each position: {(row, col): count}
    path_count = {start: 1}

    # Process row by row from top to bottom
    for row in range(start[0], rows):
        next_path_count = {}

        for (r, c), count in path_count.items():
            if r != row:
                continue

            # Try to move down
            next_row = r + 1

            # Check if we exit the manifold
            if next_row >= rows:
                # Count this as exit paths
                if ('EXIT', c) not in next_path_count:
                    next_path_count[('EXIT', c)] = 0
                next_path_count[('EXIT', c)] += count
                continue

            # Check if out of bounds (left/right)
            if c < 0 or c >= cols:
                if ('EXIT', c) not in next_path_count:
                    next_path_count[('EXIT', c)] = 0
                next_path_count[('EXIT', c)] += count
                continue

            # Check what's at the next position
            next_char = grid[next_row][c]

            if next_char == '.':
                # Continue moving down
                if (next_row, c) not in next_path_count:
                    next_path_count[(next_row, c)] = 0
                next_path_count[(next_row, c)] += count
            elif next_char == '^':
                # Split! Count paths going both ways
                # Left path
                left_col = c - 1
                if (next_row, left_col) not in next_path_count:
                    next_path_count[(next_row, left_col)] = 0
                next_path_count[(next_row, left_col)] += count

                # Right path
                right_col = c + 1
                if (next_row, right_col) not in next_path_count:
                    next_path_count[(next_row, right_col)] = 0
                next_path_count[(next_row, right_col)] += count
            elif next_char == 'S':
                # Treat S as empty space
                if (next_row, c) not in next_path_count:
                    next_path_count[(next_row, c)] = 0
                next_path_count[(next_row, c)] += count

        # Merge new paths into main count
        for pos, count in next_path_count.items():
            if pos not in path_count:
                path_count[pos] = 0
            path_count[pos] = count

    # Sum all exit path counts
    total_paths = sum(count for (r, c), count in path_count.items() if r == 'EXIT')
    return total_paths


def solve(input_file='input.txt'):
    """Solve Part 1: count beam splits."""
    with open(input_file, 'r') as f:
        grid = [line.rstrip('\n') for line in f]

    return simulate_beams(grid)


def solve_part2(input_file='input.txt'):
    """Solve Part 2: count unique timelines."""
    with open(input_file, 'r') as f:
        grid = [line.rstrip('\n') for line in f]

    return simulate_quantum_particle(grid)


def main():
    result1 = solve()
    print(f"Part 1 - Number of beam splits: {result1}")

    result2 = solve_part2()
    print(f"Part 2 - Number of unique timelines: {result2}")


if __name__ == "__main__":
    main()
