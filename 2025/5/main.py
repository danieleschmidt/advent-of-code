def parse_input(input_file='input.txt'):
    """Parse the input file into fresh ranges and available IDs."""
    with open(input_file, 'r') as f:
        content = f.read()

    sections = content.split('\n\n')

    # Parse fresh ranges
    fresh_ranges = []
    for line in sections[0].strip().split('\n'):
        start, end = line.split('-')
        fresh_ranges.append((int(start), int(end)))

    # Parse available IDs
    available_ids = []
    for line in sections[1].strip().split('\n'):
        if line:
            available_ids.append(int(line))

    return fresh_ranges, available_ids


def is_fresh(ingredient_id, fresh_ranges):
    """Check if an ingredient ID falls within any fresh range."""
    for start, end in fresh_ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def merge_ranges(ranges):
    """Merge overlapping ranges and return the merged list."""
    if not ranges:
        return []

    # Sort ranges by start position
    sorted_ranges = sorted(ranges)

    merged = [sorted_ranges[0]]

    for current_start, current_end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]

        # Check if ranges overlap or are adjacent
        if current_start <= last_end + 1:
            # Merge by extending the last range
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            # No overlap, add as new range
            merged.append((current_start, current_end))

    return merged


def count_range_coverage(ranges):
    """Count the total number of IDs covered by the ranges."""
    merged = merge_ranges(ranges)
    total = 0
    for start, end in merged:
        total += (end - start + 1)
    return total


def solve(input_file='input.txt'):
    """Solve Part 1: count fresh IDs from available list."""
    fresh_ranges, available_ids = parse_input(input_file)

    fresh_count = 0
    for ingredient_id in available_ids:
        if is_fresh(ingredient_id, fresh_ranges):
            fresh_count += 1

    return fresh_count


def solve_part2(input_file='input.txt'):
    """Solve Part 2: count total IDs covered by fresh ranges."""
    fresh_ranges, _ = parse_input(input_file)
    return count_range_coverage(fresh_ranges)


def main():
    result1 = solve()
    print(f"Part 1 - Fresh ingredient IDs from list: {result1}")

    result2 = solve_part2()
    print(f"Part 2 - Total IDs considered fresh: {result2}")


if __name__ == "__main__":
    main()
