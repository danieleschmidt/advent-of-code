def solve_safe_dial(rotations):
    """
    Solve the safe dial puzzle.

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


def main():
    # Test with the example from the problem
    example_rotations = [
        'L68', 'L30', 'R48', 'L5', 'R60',
        'L55', 'L1', 'L99', 'R14', 'L82'
    ]

    example_result = solve_safe_dial(example_rotations)
    print(f"Example result: {example_result}")
    print("Expected: 3")
    print()

    # Try to read the actual puzzle input
    try:
        with open('input.txt', 'r') as f:
            rotations = [line.strip() for line in f if line.strip()]

        result = solve_safe_dial(rotations)
        print(f"Puzzle answer: {result}")
    except FileNotFoundError:
        print("input.txt not found. Please download your puzzle input from Advent of Code.")
        print("Place it in a file named 'input.txt' in this directory.")


if __name__ == '__main__':
    main()
