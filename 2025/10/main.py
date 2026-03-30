import re
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


def parse_machine(line):
    """Parse a machine description line."""
    # Extract the target pattern [.##.]
    target_match = re.search(r'\[([.#]+)\]', line)
    target_str = target_match.group(1)
    target = [1 if c == '#' else 0 for c in target_str]

    # Extract button configurations (0,1,2)
    button_matches = re.findall(r'\(([0-9,]+)\)', line)
    buttons = []
    for button_str in button_matches:
        indices = [int(x) for x in button_str.split(',')]
        buttons.append(indices)

    # Extract joltage requirements {3,5,4,7}
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    joltage = []
    if joltage_match:
        joltage = [int(x) for x in joltage_match.group(1).split(',')]

    return target, buttons, joltage


def solve_machine(target, buttons):
    """Solve for minimum button presses using brute force for small cases."""
    n_lights = len(target)
    n_buttons = len(buttons)

    # For small numbers of buttons, try all combinations
    if n_buttons <= 20:  # Brute force for up to 20 buttons
        min_presses = float('inf')

        for mask in range(1 << n_buttons):
            # Convert mask to button presses
            button_presses = [(mask >> i) & 1 for i in range(n_buttons)]

            # Simulate the result
            lights = [0] * n_lights
            for button_idx in range(n_buttons):
                if button_presses[button_idx] == 1:
                    for light_idx in buttons[button_idx]:
                        lights[light_idx] ^= 1

            # Check if this matches the target
            if lights == target:
                presses = sum(button_presses)
                min_presses = min(min_presses, presses)

        return min_presses if min_presses != float('inf') else 0

    # For larger cases, fall back to RREF (may not be optimal)
    return solve_machine_rref(target, buttons)


def solve_machine_rref(target, buttons):
    """Solve using RREF - may not find minimum but works for large cases."""
    n_lights = len(target)
    n_buttons = len(buttons)

    matrix = []
    for light_idx in range(n_lights):
        row = []
        for button_idx in range(n_buttons):
            if light_idx in buttons[button_idx]:
                row.append(1)
            else:
                row.append(0)
        row.append(target[light_idx])
        matrix.append(row)

    # Reduce to RREF
    current_row = 0
    for col in range(n_buttons):
        pivot_row = None
        for row in range(current_row, n_lights):
            if matrix[row][col] == 1:
                pivot_row = row
                break

        if pivot_row is None:
            continue

        if pivot_row != current_row:
            matrix[current_row], matrix[pivot_row] = matrix[pivot_row], matrix[current_row]

        for row in range(n_lights):
            if row != current_row and matrix[row][col] == 1:
                for c in range(n_buttons + 1):
                    matrix[row][c] ^= matrix[current_row][c]

        current_row += 1
        if current_row >= n_lights:
            break

    # Check for inconsistency
    for row in range(n_lights):
        all_zero = all(matrix[row][col] == 0 for col in range(n_buttons))
        if all_zero and matrix[row][-1] == 1:
            return float('inf')

    # Extract solution
    solution = [0] * n_buttons
    for row in range(n_lights):
        leading_col = None
        for col in range(n_buttons):
            if matrix[row][col] == 1:
                leading_col = col
                break

        if leading_col is not None:
            solution[leading_col] = matrix[row][-1]

    return sum(solution)


def solve_machine_joltage(joltage_target, buttons):
    """Solve for minimum button presses using MILP."""
    if not joltage_target:
        return 0

    n_buttons = len(buttons)
    n_counters = len(joltage_target)

    if n_buttons == 0:
        return 0 if all(j == 0 for j in joltage_target) else float('inf')

    # Build constraint matrix A where A[i][j] = 1 if button j affects counter i
    A = np.zeros((n_counters, n_buttons))
    for button_idx, button in enumerate(buttons):
        for counter_idx in button:
            if counter_idx < n_counters:
                A[counter_idx][button_idx] = 1

    # Target values for each counter
    b = np.array(joltage_target, dtype=float)

    # Objective: minimize sum of button presses
    c = np.ones(n_buttons)

    # Constraints: A @ x == b (each counter must equal its target)
    constraints = LinearConstraint(A, b, b)

    # Bounds: x >= 0 (non-negative button presses)
    bounds = Bounds(lb=0, ub=np.inf)

    # Integrality: all variables must be integers
    integrality = np.ones(n_buttons)

    # Solve
    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)

    if result.success:
        return int(round(result.fun))
    else:
        return float('inf')


def solve(input_file='input.txt'):
    """Solve Part 1: minimum button presses for light configuration."""
    total_presses = 0

    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                target, buttons, _ = parse_machine(line)
                presses = solve_machine(target, buttons)
                total_presses += presses

    return total_presses


def solve_part2(input_file='input.txt'):
    """Solve Part 2: minimum button presses for joltage configuration."""
    total_presses = 0

    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                _, buttons, joltage = parse_machine(line)
                presses = solve_machine_joltage(joltage, buttons)
                total_presses += presses

    return total_presses


def main():
    result1 = solve()
    print(f"Part 1 - Minimum button presses (lights): {result1}")

    result2 = solve_part2()
    print(f"Part 2 - Minimum button presses (joltage): {result2}")


if __name__ == "__main__":
    main()
