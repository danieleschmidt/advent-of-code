def solve_safe_dial_debug(rotations, verbose=False):
    """
    Solve the safe dial puzzle with detailed debugging.

    Args:
        rotations: List of rotation strings (e.g., ['L68', 'R48', ...])
        verbose: If True, print detailed step-by-step trace

    Returns:
        Number of times the dial points to 0 after any rotation
    """
    position = 50  # Starting position
    zero_count = 0

    if verbose:
        print("=" * 70)
        print("DETAILED TRACE OF DIAL MOVEMENTS")
        print("=" * 70)
        print(f"Initial position: {position}")
        print()

    for i, rotation in enumerate(rotations):
        direction = rotation[0]
        distance = int(rotation[1:])
        old_position = position

        if direction == 'L':
            # Left means subtract (toward lower numbers)
            raw_value = position - distance
            position = raw_value % 100

            if verbose:
                print(f"Step {i+1}: {rotation}")
                print(f"  Direction: LEFT (toward lower numbers)")
                print(f"  Distance: {distance}")
                print(f"  Calculation: {old_position} - {distance} = {raw_value}")
                if raw_value < 0:
                    print(f"  Wrap-around: {raw_value} % 100 = {position}")
                else:
                    print(f"  Result: {position}")

        elif direction == 'R':
            # Right means add (toward higher numbers)
            raw_value = position + distance
            position = raw_value % 100

            if verbose:
                print(f"Step {i+1}: {rotation}")
                print(f"  Direction: RIGHT (toward higher numbers)")
                print(f"  Distance: {distance}")
                print(f"  Calculation: {old_position} + {distance} = {raw_value}")
                if raw_value >= 100:
                    print(f"  Wrap-around: {raw_value} % 100 = {position}")
                else:
                    print(f"  Result: {position}")

        # Count if we land on 0
        if position == 0:
            zero_count += 1
            if verbose:
                print(f"  >>> LANDED ON 0! (Total count: {zero_count})")

        if verbose:
            print()

    if verbose:
        print("=" * 70)
        print(f"FINAL RESULT: Dial landed on 0 a total of {zero_count} times")
        print("=" * 70)

    return zero_count


def test_modulo_behavior():
    """Test Python's modulo behavior with negative numbers."""
    print("=" * 70)
    print("TESTING PYTHON MODULO BEHAVIOR")
    print("=" * 70)

    test_cases = [
        (-18, 100, 82),  # From example: 50 - 68
        (-5, 100, 95),   # From example: 0 - 5
        (-1, 100, 99),   # From example: 0 - 1
        (-68, 100, 32),  # From example: 14 - 82
        (100, 100, 0),   # Going right from 52
        (155, 100, 55),  # From example: 95 + 60
    ]

    all_passed = True
    for value, mod, expected in test_cases:
        result = value % mod
        status = "✓" if result == expected else "✗"
        print(f"{status} {value} % {mod} = {result} (expected {expected})")
        if result != expected:
            all_passed = False

    print()
    if all_passed:
        print("✓ All modulo tests PASSED")
    else:
        print("✗ Some modulo tests FAILED")
    print("=" * 70)
    print()


def verify_example():
    """Verify the example from the problem statement."""
    print("=" * 70)
    print("VERIFYING EXAMPLE FROM PROBLEM STATEMENT")
    print("=" * 70)
    print()

    example_rotations = [
        'L68', 'L30', 'R48', 'L5', 'R60',
        'L55', 'L1', 'L99', 'R14', 'L82'
    ]

    expected_positions = [82, 52, 0, 95, 55, 0, 99, 0, 14, 32]
    expected_zero_count = 3

    result = solve_safe_dial_debug(example_rotations, verbose=True)

    print()
    print(f"Expected zero count: {expected_zero_count}")
    print(f"Actual zero count: {result}")

    if result == expected_zero_count:
        print("✓ EXAMPLE VERIFICATION PASSED!")
    else:
        print("✗ EXAMPLE VERIFICATION FAILED!")

    print()


def analyze_input_file():
    """Analyze the actual input file."""
    print("=" * 70)
    print("ANALYZING INPUT FILE")
    print("=" * 70)

    try:
        with open('input.txt', 'r') as f:
            lines = f.readlines()

        print(f"Total lines in file: {len(lines)}")

        rotations = [line.strip() for line in lines if line.strip()]
        print(f"Non-empty lines (rotations): {len(rotations)}")
        print()

        # Analyze rotation types
        left_count = sum(1 for r in rotations if r.startswith('L'))
        right_count = sum(1 for r in rotations if r.startswith('R'))

        print(f"Left rotations (L): {left_count}")
        print(f"Right rotations (R): {right_count}")
        print()

        # Show first and last few rotations
        print("First 10 rotations:")
        for i, rot in enumerate(rotations[:10], 1):
            print(f"  {i}. {rot}")
        print()

        print("Last 10 rotations:")
        for i, rot in enumerate(rotations[-10:], len(rotations)-9):
            print(f"  {i}. {rot}")
        print()

        # Check for any invalid formats
        invalid = []
        for i, rot in enumerate(rotations, 1):
            if not rot or rot[0] not in ['L', 'R']:
                invalid.append((i, rot))
            else:
                try:
                    int(rot[1:])
                except ValueError:
                    invalid.append((i, rot))

        if invalid:
            print(f"⚠ Found {len(invalid)} invalid rotation(s):")
            for line_num, rot in invalid[:5]:
                print(f"  Line {line_num}: '{rot}'")
        else:
            print("✓ All rotations have valid format")

        print("=" * 70)
        print()

        return rotations

    except FileNotFoundError:
        print("✗ input.txt not found!")
        return None


def main():
    # Test 1: Verify Python modulo behavior
    test_modulo_behavior()

    # Test 2: Verify example
    verify_example()

    # Test 3: Analyze input file
    rotations = analyze_input_file()

    if rotations:
        # Test 4: Run on actual input
        print("=" * 70)
        print("RUNNING ON ACTUAL INPUT")
        print("=" * 70)
        print("(Running without verbose trace to avoid overwhelming output)")
        print()

        result = solve_safe_dial_debug(rotations, verbose=False)
        print(f"Puzzle answer: {result}")
        print("=" * 70)
        print()

        # Test 5: Spot check - show first 20 steps with trace
        print("=" * 70)
        print("SPOT CHECK: First 20 rotations with detailed trace")
        print("=" * 70)
        print()

        solve_safe_dial_debug(rotations[:20], verbose=True)


if __name__ == '__main__':
    main()
