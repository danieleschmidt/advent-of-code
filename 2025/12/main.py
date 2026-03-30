def parse_input(input_file='input.txt'):
    """Parse shapes and regions from input."""
    with open(input_file, 'r') as f:
        content = f.read()

    sections = content.split('\n\n')

    # Parse shapes
    shapes = {}
    shape_idx = 0
    for section in sections[:-1]:  # All but last section are shapes
        lines = section.strip().split('\n')
        if lines and ':' in lines[0]:
            idx = int(lines[0].rstrip(':'))
            shape_grid = []
            for line in lines[1:]:
                shape_grid.append(list(line))
            shapes[idx] = shape_grid
            shape_idx += 1

    # Parse regions
    regions = []
    for line in sections[-1].strip().split('\n'):
        if line:
            parts = line.split(': ')
            dims = parts[0].split('x')
            width, height = int(dims[0]), int(dims[1])
            counts = list(map(int, parts[1].split()))
            regions.append((width, height, counts))

    return shapes, regions


def get_shape_cells(shape):
    """Get list of (row, col) coordinates where shape has '#'."""
    cells = []
    for r in range(len(shape)):
        for c in range(len(shape[r])):
            if shape[r][c] == '#':
                cells.append((r, c))
    return cells


def normalize_cells(cells):
    """Normalize cell coordinates to start from (0, 0)."""
    if not cells:
        return []
    min_r = min(r for r, c in cells)
    min_c = min(c for r, c in cells)
    return tuple(sorted((r - min_r, c - min_c) for r, c in cells))


def rotate_90(cells):
    """Rotate cells 90 degrees clockwise."""
    return [(c, -r) for r, c in cells]


def flip_h(cells):
    """Flip cells horizontally."""
    return [(-r, c) for r, c in cells]


def get_all_orientations(shape):
    """Get all unique orientations (rotations and flips) of a shape."""
    cells = get_shape_cells(shape)
    orientations = set()

    # Original
    current = cells
    for _ in range(4):  # 4 rotations
        normalized = normalize_cells(current)
        orientations.add(normalized)
        current = rotate_90(current)

    # Flipped
    current = flip_h(cells)
    for _ in range(4):  # 4 rotations of flipped
        normalized = normalize_cells(current)
        orientations.add(normalized)
        current = rotate_90(current)

    return list(orientations)


def can_place(grid, cells, start_r, start_c):
    """Check if shape can be placed at given position."""
    rows, cols = len(grid), len(grid[0])

    for dr, dc in cells:
        r, c = start_r + dr, start_c + dc
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if grid[r][c] == 1:  # Already occupied
            return False

    return True


def place(grid, cells, start_r, start_c, value):
    """Place or remove shape on grid."""
    for dr, dc in cells:
        r, c = start_r + dr, start_c + dc
        grid[r][c] = value


def solve_region_backtrack(grid, presents_to_place, all_orientations, present_sizes, idx=0):
    """Try to place all presents using backtracking with optimizations."""
    if idx >= len(presents_to_place):
        return True  # All presents placed successfully

    shape_idx = presents_to_place[idx]

    rows, cols = len(grid), len(grid[0])

    # Calculate remaining space needed
    remaining_cells_needed = sum(present_sizes[presents_to_place[i]] for i in range(idx, len(presents_to_place)))
    available_cells = sum(1 for r in range(rows) for c in range(cols) if grid[r][c] == 0)

    if available_cells < remaining_cells_needed:
        return False  # Not enough space

    # Try all orientations of this present
    for cells in all_orientations[shape_idx]:
        # Calculate bounds of this orientation
        max_r = max(r for r, c in cells)
        max_c = max(c for r, c in cells)

        # Try all positions (only where shape can fit)
        for r in range(rows - max_r):
            for c in range(cols - max_c):
                if can_place(grid, cells, r, c):
                    # Place the present
                    place(grid, cells, r, c, 1)

                    # Recursively try to place the rest
                    if solve_region_backtrack(grid, presents_to_place, all_orientations, present_sizes, idx + 1):
                        return True

                    # Backtrack
                    place(grid, cells, r, c, 0)

    return False


def can_fit_region(width, height, counts, shapes):
    """Check if all presents can fit in the region."""
    # Generate all orientations for each shape
    all_orientations = {}
    present_sizes = {}
    for shape_idx in shapes:
        all_orientations[shape_idx] = get_all_orientations(shapes[shape_idx])
        # Calculate size (number of # cells)
        present_sizes[shape_idx] = len(get_shape_cells(shapes[shape_idx]))

    # Build list of presents to place (shape indices, one per present)
    presents_to_place = []
    for shape_idx, count in enumerate(counts):
        for _ in range(count):
            presents_to_place.append(shape_idx)

    # Sort presents by size (largest first) for better pruning
    presents_to_place.sort(key=lambda idx: present_sizes.get(idx, 0), reverse=True)

    # Create empty grid
    grid = [[0] * width for _ in range(height)]

    # Try to place all presents
    return solve_region_backtrack(grid, presents_to_place, all_orientations, present_sizes)


def solve(input_file='input.txt'):
    """Count how many regions can fit all their presents."""
    shapes, regions = parse_input(input_file)

    count = 0
    for width, height, counts in regions:
        if can_fit_region(width, height, counts, shapes):
            count += 1

    return count


def main():
    result = solve()
    print(f"Number of regions that can fit all presents: {result}")


if __name__ == "__main__":
    main()
