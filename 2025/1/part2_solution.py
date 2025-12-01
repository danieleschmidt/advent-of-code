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
        # Moving right: we pass through position+1, position+2, ..., position+distance
        # Count how many multiples of 100 are in (position, position+distance]
        # Formula: floor((position + distance) / 100) - floor(position / 100)
        return (position + distance) // 100 - position // 100

    elif direction == 'L':
        # Moving left: we pass through position-1, position-2, ..., position-distance
        # Count how many multiples of 100 are in [position-distance, position)
        # Formula: floor((position - 1) / 100) - floor((position - distance - 1) / 100)
        return (position - 1) // 100 - (position - distance - 1) // 100

    return 0


def solve_safe_dial_part2(rotations, verbose=False):
    """
    Solve the safe dial puzzle part 2.

    Count every time the dial passes through 0, including during rotations.

    Args:
        rotations: List of rotation strings (e.g., ['L68', 'R48', ...])
        verbose: If True, print detailed trace

    Returns:
        Number of times the dial points to 0 (during and after rotations)
    """
    position = 50  # Starting position
    zero_count = 0

    if verbose:
        print("=" * 70)
        print("PART 2: Counting zeros during and after rotations")
        print("=" * 70)
        print(f"Initial position: {position}")
        print()

    for i, rotation in enumerate(rotations):
        direction = rotation[0]
        distance = int(rotation[1:])
        old_position = position

        # Count zeros during this rotation
        zeros_in_rotation = count_zeros_during_rotation(position, direction, distance)
        zero_count += zeros_in_rotation

        # Calculate final position
        if direction == 'L':
            position = (position - distance) % 100
        elif direction == 'R':
            position = (position + distance) % 100

        if verbose:
            print(f"Step {i+1}: {rotation}")
            print(f"  From {old_position} to {position}")
            if zeros_in_rotation > 0:
                print(f"  >>> Passed through 0 {zeros_in_rotation} time(s) (Total: {zero_count})")
            else:
                print(f"  No zeros during this rotation")
            print()

    if verbose:
        print("=" * 70)
        print(f"TOTAL: Dial pointed at 0 {zero_count} times")
        print("=" * 70)

    return zero_count


def test_zero_counting():
    """Test the zero counting logic with various cases."""
    print("=" * 70)
    print("TESTING ZERO COUNTING DURING ROTATIONS")
    print("=" * 70)
    print()

    test_cases = [
        # (position, direction, distance, expected_count, description)
        (50, 'L', 68, 1, "L68 from 50 → 82 (passes through 0 once)"),
        (82, 'L', 30, 0, "L30 from 82 → 52 (no zeros)"),
        (52, 'R', 48, 1, "R48 from 52 → 0 (ends at 0)"),
        (0, 'L', 5, 0, "L5 from 0 → 95 (starts at 0, doesn't pass through)"),
        (95, 'R', 60, 1, "R60 from 95 → 55 (passes through 0 once)"),
        (55, 'L', 55, 1, "L55 from 55 → 0 (ends at 0)"),
        (0, 'L', 1, 0, "L1 from 0 → 99 (no zeros)"),
        (99, 'L', 99, 1, "L99 from 99 → 0 (ends at 0)"),
        (0, 'R', 14, 0, "R14 from 0 → 14 (no zeros)"),
        (14, 'L', 82, 1, "L82 from 14 → 32 (passes through 0 once)"),
        (50, 'R', 1000, 10, "R1000 from 50 → 50 (passes through 0 ten times!)"),
    ]

    all_passed = True
    for pos, direction, distance, expected, description in test_cases:
        result = count_zeros_during_rotation(pos, direction, distance)
        final_pos = (pos + distance) % 100 if direction == 'R' else (pos - distance) % 100
        status = "✓" if result == expected else "✗"

        print(f"{status} {description}")
        print(f"   Count: {result}, Expected: {expected}")

        if result != expected:
            all_passed = False
            print(f"   ERROR: Got {result}, expected {expected}")
        print()

    if all_passed:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")

    print("=" * 70)
    print()

    return all_passed


def verify_example():
    """Verify the example from part 2."""
    print("=" * 70)
    print("VERIFYING PART 2 EXAMPLE")
    print("=" * 70)
    print()

    example_rotations = [
        'L68', 'L30', 'R48', 'L5', 'R60',
        'L55', 'L1', 'L99', 'R14', 'L82'
    ]

    result = solve_safe_dial_part2(example_rotations, verbose=True)

    print()
    print(f"Expected: 6")
    print(f"Got: {result}")

    if result == 6:
        print("✓ EXAMPLE VERIFICATION PASSED!")
        return True
    else:
        print("✗ EXAMPLE VERIFICATION FAILED!")
        return False


def main():
    # Test 1: Test zero counting logic
    tests_passed = test_zero_counting()

    if not tests_passed:
        print("⚠ Tests failed, but continuing...")
        print()

    # Test 2: Verify example
    example_passed = verify_example()

    if not example_passed:
        print("⚠ Example verification failed!")
        return

    # Test 3: Run on actual input
    print()
    print("=" * 70)
    print("RUNNING ON ACTUAL INPUT")
    print("=" * 70)
    print()

    try:
        with open('input.txt', 'r') as f:
            rotations = [line.strip() for line in f if line.strip()]

        print(f"Processing {len(rotations)} rotations...")
        result = solve_safe_dial_part2(rotations, verbose=False)

        print()
        print("=" * 70)
        print(f"PART 2 ANSWER: {result}")
        print("=" * 70)

    except FileNotFoundError:
        print("input.txt not found!")


if __name__ == '__main__':
    main()
