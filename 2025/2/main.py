def is_invalid_id(num):
    """Check if a number is an invalid ID (repeated pattern of digits at least twice)."""
    s = str(num)

    # Check for leading zeros (though our ranges shouldn't have these)
    if s[0] == '0':
        return False

    # Try all possible pattern lengths from 1 to len(s)//2
    # Pattern must repeat at least twice
    for pattern_len in range(1, len(s) // 2 + 1):
        # String length must be divisible by pattern length
        if len(s) % pattern_len == 0:
            pattern = s[:pattern_len]
            # Check if repeating this pattern creates the entire string
            repetitions = len(s) // pattern_len
            if pattern * repetitions == s and repetitions >= 2:
                return True

    return False


def parse_ranges(input_str):
    """Parse the comma-separated ranges from input."""
    ranges = []
    parts = input_str.strip().split(',')
    for part in parts:
        part = part.strip()
        if part:
            start, end = part.split('-')
            ranges.append((int(start), int(end)))
    return ranges


def find_invalid_ids(ranges):
    """Find all invalid IDs across all ranges."""
    invalid_ids = []

    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid_id(num):
                invalid_ids.append(num)

    return invalid_ids


def main():
    # Read input
    with open('input.txt', 'r') as f:
        input_data = f.read()

    # Parse ranges
    ranges = parse_ranges(input_data)

    # Find all invalid IDs
    invalid_ids = find_invalid_ids(ranges)

    # Calculate sum
    total = sum(invalid_ids)

    print(f"Found {len(invalid_ids)} invalid IDs")
    print(f"Sum of all invalid IDs: {total}")


if __name__ == "__main__":
    main()
