def parse_worksheet(input_file='input.txt'):
    """Parse the worksheet and extract problems."""
    with open(input_file, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    # Remove blank lines at the end
    while lines and not lines[-1].strip():
        lines.pop()

    if not lines:
        return []

    # The operator line is the last line
    operator_line = lines[-1]

    # Number lines are all lines except the last one
    number_lines = lines[:-1]

    # Find the width of the worksheet
    max_width = max(len(line) for line in lines)

    # Pad all lines to the same width
    padded_number_lines = [line.ljust(max_width) for line in number_lines]
    padded_operator_line = operator_line.ljust(max_width)

    # Identify problem blocks by finding where all rows have only spaces
    problem_blocks = []
    start_col = None

    for col in range(max_width):
        # Check if this column is all spaces in all rows
        is_blank = all(padded_number_lines[row][col] == ' ' for row in range(len(padded_number_lines)))
        is_blank = is_blank and padded_operator_line[col] == ' '

        if not is_blank:
            if start_col is None:
                start_col = col
        else:
            if start_col is not None:
                problem_blocks.append((start_col, col))
                start_col = None

    # Handle the last block
    if start_col is not None:
        problem_blocks.append((start_col, max_width))

    problems = []

    for start, end in problem_blocks:
        # Extract the operator for this block (should be near the end)
        operator = None
        for c in range(start, end):
            if padded_operator_line[c] in ['+', '*']:
                operator = padded_operator_line[c]
                break

        if not operator:
            continue

        # Extract numbers from each row in this block
        numbers = []
        for row_line in padded_number_lines:
            # Get the substring for this block and extract the number
            block_text = row_line[start:end].strip()
            if block_text:
                try:
                    numbers.append(int(block_text))
                except ValueError:
                    pass

        if numbers and operator:
            problems.append((numbers, operator))

    return problems


def solve_problem(numbers, operator):
    """Solve a single problem by applying the operator to all numbers."""
    if operator == '+':
        return sum(numbers)
    elif operator == '*':
        result = 1
        for num in numbers:
            result *= num
        return result
    return 0


def parse_worksheet_rtl(input_file='input.txt'):
    """Parse worksheet reading right-to-left (Part 2)."""
    with open(input_file, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    # Remove blank lines at the end
    while lines and not lines[-1].strip():
        lines.pop()

    if not lines:
        return []

    # The operator line is the last line
    operator_line = lines[-1]

    # Number lines are all lines except the last one
    number_lines = lines[:-1]

    # Find the width of the worksheet
    max_width = max(len(line) for line in lines)

    # Pad all lines to the same width, then REVERSE each line
    padded_number_lines = [line.ljust(max_width)[::-1] for line in number_lines]
    padded_operator_line = operator_line.ljust(max_width)[::-1]

    # Identify problem blocks by finding where all rows have only spaces
    problem_blocks = []
    start_col = None

    for col in range(max_width):
        # Check if this column is all spaces in all rows
        is_blank = all(padded_number_lines[row][col] == ' ' for row in range(len(padded_number_lines)))
        is_blank = is_blank and padded_operator_line[col] == ' '

        if not is_blank:
            if start_col is None:
                start_col = col
        else:
            if start_col is not None:
                problem_blocks.append((start_col, col))
                start_col = None

    # Handle the last block
    if start_col is not None:
        problem_blocks.append((start_col, max_width))

    problems = []

    for start, end in problem_blocks:
        # Extract the operator for this block
        operator = None
        for c in range(start, end):
            if padded_operator_line[c] in ['+', '*']:
                operator = padded_operator_line[c]
                break

        if not operator:
            continue

        # Extract numbers by reading columns top-to-bottom
        numbers = []
        for col in range(start, end):
            # Read this column top to bottom to build a number
            num_str = ''
            for row_line in padded_number_lines:
                if col < len(row_line) and row_line[col].isdigit():
                    num_str += row_line[col]

            if num_str:
                numbers.append(int(num_str))

        if numbers and operator:
            problems.append((numbers, operator))

    return problems


def solve(input_file='input.txt'):
    """Solve Part 1: left-to-right reading."""
    problems = parse_worksheet(input_file)

    grand_total = 0
    for numbers, operator in problems:
        result = solve_problem(numbers, operator)
        grand_total += result

    return grand_total


def solve_part2(input_file='input.txt'):
    """Solve Part 2: right-to-left reading."""
    problems = parse_worksheet_rtl(input_file)

    grand_total = 0
    for numbers, operator in problems:
        result = solve_problem(numbers, operator)
        grand_total += result

    return grand_total


def main():
    result1 = solve()
    print(f"Part 1 - Grand total (left-to-right): {result1}")

    result2 = solve_part2()
    print(f"Part 2 - Grand total (right-to-left): {result2}")


if __name__ == "__main__":
    main()
