def find_max_joltage(bank, num_batteries=2):
    """
    Find the maximum joltage by selecting exactly num_batteries from the bank.
    Uses a greedy algorithm to find the lexicographically largest subsequence.
    """
    n = len(bank)
    result = []
    current_pos = 0

    # For each position in the result
    for i in range(num_batteries):
        # We need (num_batteries - i) more digits including this one
        remaining_needed = num_batteries - i
        # We must leave enough digits after our choice
        max_search_pos = n - remaining_needed + 1

        # Find the largest digit in the valid range
        best_digit = '0'
        best_pos = current_pos

        for pos in range(current_pos, max_search_pos):
            if bank[pos] > best_digit:
                best_digit = bank[pos]
                best_pos = pos

        result.append(best_digit)
        current_pos = best_pos + 1

    return int(''.join(result))


def solve(input_data, num_batteries=2):
    """Solve the puzzle and return the total output joltage."""
    banks = input_data.strip().split('\n')
    total_joltage = 0

    for bank in banks:
        if bank:  # Skip empty lines
            max_jolt = find_max_joltage(bank, num_batteries)
            total_joltage += max_jolt

    return total_joltage


def main():
    # Read input
    with open('input.txt', 'r') as f:
        input_data = f.read()

    # Solve Part 1
    print("Part 1 (2 batteries):")
    result1 = solve(input_data, num_batteries=2)
    print(f"Total output joltage: {result1}\n")

    # Solve Part 2
    print("Part 2 (12 batteries):")
    result2 = solve(input_data, num_batteries=12)
    print(f"Total output joltage: {result2}")


if __name__ == "__main__":
    main()
