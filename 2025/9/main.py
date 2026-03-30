def parse_input(input_file='input.txt'):
    """Parse the input file to get red tile coordinates."""
    tiles = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(int, line.split(','))
                tiles.append((x, y))
    return tiles


def calculate_area(tile1, tile2):
    """Calculate the area of a rectangle with opposite corners at tile1 and tile2."""
    x1, y1 = tile1
    x2, y2 = tile2
    # Add 1 to each dimension because the corners are inclusive
    width = abs(x2 - x1) + 1
    height = abs(y2 - y1) + 1
    return width * height


def build_green_tiles_optimized(red_tiles):
    """Build set of all green tiles more efficiently."""
    green_tiles = set()

    # Add tiles on the path connecting consecutive red tiles
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % len(red_tiles)]  # Wrap around

        # Add all tiles between these two red tiles
        if x1 == x2:  # Same column
            for y in range(min(y1, y2), max(y1, y2) + 1):
                green_tiles.add((x1, y))
        elif y1 == y2:  # Same row
            for x in range(min(x1, x2), max(x1, x2) + 1):
                green_tiles.add((x, y1))

    # Remove red tiles from green tiles
    for tile in red_tiles:
        green_tiles.discard(tile)

    # Build the polygon boundary more efficiently
    # Use scanline algorithm instead of checking every point
    boundary_tiles = set(red_tiles) | green_tiles

    # Get bounding box
    all_x = [x for x, y in red_tiles]
    all_y = [y for x, y in red_tiles]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # Find an interior point to start flood fill
    # Use a scanline to find first interior point efficiently
    from collections import deque

    start_point = None
    # For each row, find transitions from outside to inside
    for try_y in range(min_y + 1, max_y):
        row_boundary_x = sorted([x for x, y in boundary_tiles if y == try_y])
        if len(row_boundary_x) >= 2:
            # Try a point between first two boundary x coords
            test_x = row_boundary_x[0] + 1
            if test_x < row_boundary_x[1]:
                test_point = (test_x, try_y)
                if test_point not in boundary_tiles:
                    start_point = test_point
                    break

    # Do flood fill from interior point if found
    # Once inside, just avoid boundary tiles - no need for polygon check each time
    if start_point:
        queue = deque([start_point])
        visited_fill = {start_point}

        while queue:
            x, y = queue.popleft()
            green_tiles.add((x, y))

            # Check 4 neighbors
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited_fill and (nx, ny) not in boundary_tiles:
                    visited_fill.add((nx, ny))
                    queue.append((nx, ny))

    return green_tiles


def is_inside_polygon(point, polygon):
    """Check if a point is inside a polygon using ray casting."""
    x, y = point
    n = len(polygon)
    inside = False

    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]

        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside

        j = i

    return inside


def is_on_boundary(point, red_tiles):
    """Check if a point is on the boundary path between consecutive red tiles."""
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % len(red_tiles)]

        x, y = point

        # Check if point is on the line segment between these two red tiles
        if x1 == x2 and x == x1:  # Vertical line
            if min(y1, y2) <= y <= max(y1, y2):
                return True
        elif y1 == y2 and y == y1:  # Horizontal line
            if min(x1, x2) <= x <= max(x1, x2):
                return True

    return False


def is_valid_tile_part2(point, red_tile_set, red_tiles):
    """Check if a tile is red or green (on boundary or inside polygon)."""
    if point in red_tile_set:
        return True
    if is_on_boundary(point, red_tiles):
        return True
    if is_inside_polygon(point, red_tiles):
        return True
    return False


def is_strictly_inside(point, red_tile_set, red_tiles):
    """Check if a point is strictly inside (not on boundary, not red)."""
    if point in red_tile_set:
        return False
    if is_on_boundary(point, red_tiles):
        return False
    return is_inside_polygon(point, red_tiles)


def is_valid_rectangle_part2(tile1, tile2, red_tile_set, red_tiles):
    """Check if rectangle only contains red or green tiles."""
    x1, y1 = tile1
    x2, y2 = tile2

    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    # Do full check - with early termination for efficiency
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if not is_valid_tile_part2((x, y), red_tile_set, red_tiles):
                return False

    return True


def solve(input_file='input.txt'):
    """Find the largest rectangle area using red tiles as opposite corners."""
    tiles = parse_input(input_file)

    max_area = 0

    # Try all pairs of tiles as opposite corners
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            area = calculate_area(tiles[i], tiles[j])
            max_area = max(max_area, area)

    return max_area


def edge_intersects_rect(x1, y1, x2, y2, rx_min, ry_min, rx_max, ry_max):
    """Check if a polygon edge crosses through the rectangle's interior (not boundary)."""
    if x1 == x2:  # Vertical edge
        # Edge crosses interior if its x is strictly between rect's x bounds
        if rx_min < x1 < rx_max:
            # And if edge's y range overlaps rect's y range
            seg_y_min, seg_y_max = min(y1, y2), max(y1, y2)
            if seg_y_min < ry_max and seg_y_max > ry_min:
                return True
    elif y1 == y2:  # Horizontal edge
        # Edge crosses interior if its y is strictly between rect's y bounds
        if ry_min < y1 < ry_max:
            # And if edge's x range overlaps rect's x range
            seg_x_min, seg_x_max = min(x1, x2), max(x1, x2)
            if seg_x_min < rx_max and seg_x_max > rx_min:
                return True
    return False


def solve_part2(input_file='input.txt'):
    """Find largest rectangle using only red and green tiles."""
    red_tiles = parse_input(input_file)
    red_tile_set = set(red_tiles)

    max_area = 0

    # Try all pairs of red tiles as opposite corners
    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]

            rx_min, rx_max = min(x1, x2), max(x1, x2)
            ry_min, ry_max = min(y1, y2), max(y1, y2)

            # Check all 4 corners are inside polygon or are red tiles
            corners = [(rx_min, ry_min), (rx_min, ry_max), (rx_max, ry_min), (rx_max, ry_max)]
            valid = True
            for cx, cy in corners:
                if (cx, cy) not in red_tile_set:
                    if not is_inside_polygon((cx, cy), red_tiles):
                        valid = False
                        break

            if not valid:
                continue

            # Check no polygon edge crosses through rectangle interior
            for k in range(len(red_tiles)):
                ex1, ey1 = red_tiles[k]
                ex2, ey2 = red_tiles[(k + 1) % len(red_tiles)]

                if edge_intersects_rect(ex1, ey1, ex2, ey2, rx_min, ry_min, rx_max, ry_max):
                    valid = False
                    break

            if valid:
                area = (rx_max - rx_min + 1) * (ry_max - ry_min + 1)
                max_area = max(max_area, area)

    return max_area


def main():
    result1 = solve()
    print(f"Part 1 - Largest rectangle area: {result1}")

    result2 = solve_part2()
    print(f"Part 2 - Largest rectangle area (red/green only): {result2}")


if __name__ == "__main__":
    main()
