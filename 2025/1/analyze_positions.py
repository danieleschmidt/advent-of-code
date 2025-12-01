"""
Analyze the distribution of dial positions after rotations.
"""

def analyze_positions(rotations):
    """Analyze which positions the dial lands on."""
    position = 50
    position_counts = {}

    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        if direction == 'L':
            position = (position - distance) % 100
        elif direction == 'R':
            position = (position + distance) % 100

        # Count this position
        position_counts[position] = position_counts.get(position, 0) + 1

    return position_counts


def main():
    with open('input.txt', 'r') as f:
        rotations = [line.strip() for line in f if line.strip()]

    print(f"Total rotations: {len(rotations)}")
    print()

    position_counts = analyze_positions(rotations)

    print(f"Unique positions landed on: {len(position_counts)}")
    print()

    # Show top 10 most frequent positions
    print("Top 10 most frequent positions:")
    sorted_positions = sorted(position_counts.items(), key=lambda x: x[1], reverse=True)
    for i, (pos, count) in enumerate(sorted_positions[:10], 1):
        percentage = (count / len(rotations)) * 100
        print(f"  {i:2d}. Position {pos:2d}: {count:4d} times ({percentage:.2f}%)")

    print()

    # Show how many times we land on 0
    zero_count = position_counts.get(0, 0)
    zero_percentage = (zero_count / len(rotations)) * 100
    print(f"Position 0 count: {zero_count} ({zero_percentage:.2f}%)")
    print()

    # Show positions that never appear
    all_positions = set(range(100))
    landed_positions = set(position_counts.keys())
    never_landed = sorted(all_positions - landed_positions)

    if never_landed:
        print(f"Positions never landed on ({len(never_landed)}): {never_landed[:20]}")
        if len(never_landed) > 20:
            print(f"  ... and {len(never_landed) - 20} more")
    else:
        print("All positions (0-99) were landed on at least once!")

    print()
    print("=" * 70)
    print(f"ANSWER: {zero_count}")
    print("=" * 70)


if __name__ == '__main__':
    main()
