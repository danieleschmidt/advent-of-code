def solve_safe_dial_part1(rotations):
    """
    Solve the safe dial puzzle - Part 1.

    Count only when the dial ENDS at position 0 after a rotation.

    Args:
        rotations: List of rotation strings (e.g., ['L68', 'R48', ...])

    Returns:
        Number of times the dial points to 0 after any rotation
    """
    position = 50  # Starting position
    zero_count = 0

    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        if direction == 'L':
            # Left means subtract (toward lower numbers)
            position = (position - distance) % 100
        elif direction == 'R':
            # Right means add (toward higher numbers)
            position = (position + distance) % 100

        # Count if we land on 0
        if position == 0:
            zero_count += 1

    return zero_count


def count_zeros_during_rotation(position, direction, distance):
    """
    Count how many times the dial passes through 0 during a rotation.

    This includes the final position if it's 0, but not the starting position.

    Args:
        position: Current position (0-99)
        direction: 'L' for left (subtract) or 'R' for right (add)
        distance: How many clicks to rotate

    Returns:
        Number of times the dial points to 0 during this rotation
    """
    if direction == 'R':
        # Moving right: count multiples of 100 in (position, position+distance]
        return (position + distance) // 100 - position // 100
    elif direction == 'L':
        # Moving left: count multiples of 100 in [position-distance, position)
        return (position - 1) // 100 - (position - distance - 1) // 100
    return 0


def solve_safe_dial_part2(rotations):
    """
    Solve the safe dial puzzle - Part 2.

    Count EVERY time the dial passes through 0, including during rotations.

    Args:
        rotations: List of rotation strings (e.g., ['L68', 'R48', ...])

    Returns:
        Number of times the dial points to 0 (during and after rotations)
    """
    position = 50  # Starting position
    zero_count = 0

    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        # Count zeros during this rotation
        zero_count += count_zeros_during_rotation(position, direction, distance)

        # Calculate final position
        if direction == 'L':
            position = (position - distance) % 100
        elif direction == 'R':
            position = (position + distance) % 100

    return zero_count


def main():
    # Test with the example from the problem
    example_rotations = [
        'L68', 'L30', 'R48', 'L5', 'R60',
        'L55', 'L1', 'L99', 'R14', 'L82'
    ]

    print("=" * 70)
    print("PART 1: Count zeros at the END of rotations")
    print("=" * 70)
    example_result_part1 = solve_safe_dial_part1(example_rotations)
    print(f"Example result: {example_result_part1}")
    print("Expected: 3")
    print()

    print("=" * 70)
    print("PART 2: Count zeros DURING and after rotations")
    print("=" * 70)
    example_result_part2 = solve_safe_dial_part2(example_rotations)
    print(f"Example result: {example_result_part2}")
    print("Expected: 6")
    print()

    # Try to read the actual puzzle input
    try:
        with open('input.txt', 'r') as f:
            rotations = [line.strip() for line in f if line.strip()]

        print("=" * 70)
        print(f"Processing {len(rotations)} rotations from input.txt")
        print("=" * 70)

        result_part1 = solve_safe_dial_part1(rotations)
        print(f"Part 1 answer: {result_part1}")

        result_part2 = solve_safe_dial_part2(rotations)
        print(f"Part 2 answer: {result_part2}")

        print()
        print(f"Difference: {result_part2 - result_part1} additional zeros found during rotations")

    except FileNotFoundError:
        print("input.txt not found. Please download your puzzle input from Advent of Code.")
        print("Place it in a file named 'input.txt' in this directory.")


if __name__ == '__main__':
    main()
