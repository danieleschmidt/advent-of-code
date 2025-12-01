# Advent of Code 2025 - Day 1: Secret Entrance

Complete solution for both parts of the safe dial puzzle.

---

## 🎯 Answers

- **Part 1**: 1165 ✓
- **Part 2**: 6496 ✓

---

## Problem Summary

### The Puzzle
A safe has a circular dial with positions 0-99. Following rotation instructions (L for left, R for right), determine the password.

### Part 1
**Task**: Count how many times the dial ENDS at position 0 after a rotation.

**Example**: L68, L30, R48, L5, R60, L55, L1, L99, R14, L82
- Result: **3** (dial ends at 0 three times)

**Answer**: **1165**

### Part 2
**Task**: Count EVERY time the dial passes through position 0, including during rotations.

**Example**: Same rotations as Part 1
- Result: **6** (3 from Part 1, plus 3 more during rotations)

**Key Insight**: A rotation like R1000 from position 50 passes through 0 exactly 10 times!

**Answer**: **6496**

---

## Solution Approach

### Part 1: Simple Position Tracking
```python
position = 50  # Starting position
zero_count = 0

for rotation in rotations:
    if direction == 'L':
        position = (position - distance) % 100
    elif direction == 'R':
        position = (position + distance) % 100

    if position == 0:
        zero_count += 1
```

### Part 2: Counting Passes Through Zero

The key is calculating how many times we pass through 0 during a rotation.

**RIGHT Rotation** (toward higher numbers):
- From position P, moving D clicks right
- Formula: `floor((P + D) / 100) - floor(P / 100)`
- Counts multiples of 100 in range (P, P+D]

**LEFT Rotation** (toward lower numbers):
- From position P, moving D clicks left
- Formula: `floor((P - 1) / 100) - floor((P - D - 1) / 100)`
- Counts multiples of 100 in range [P-D, P)

```python
def count_zeros_during_rotation(position, direction, distance):
    if direction == 'R':
        return (position + distance) // 100 - position // 100
    elif direction == 'L':
        return (position - 1) // 100 - (position - distance - 1) // 100
    return 0
```

---

## Mathematical Proof

### Why the Formula Works

#### RIGHT Rotation Example
Position 50, rotate R1000:
- Positions visited: 51, 52, ..., 99, 0, 1, ..., 99, 0, ..., 50
- We hit 0 at: 50+50=100→0, 50+150=200→0, ..., 50+950=1000→0
- Formula: `(50 + 1000) // 100 - 50 // 100 = 10 - 0 = 10` ✓

#### LEFT Rotation Example
Position 50, rotate L68:
- Positions visited: 49, 48, ..., 1, 0, 99, ..., 82
- We hit 0 once (between 1 and 99)
- Formula: `(50 - 1) // 100 - (50 - 68 - 1) // 100 = 0 - (-1) = 1` ✓

### Python's Integer Division
Python's `//` operator with negative numbers:
- `-18 // 100 = -1` (not 0)
- `-1 // 100 = -1` (not 0)
- `49 // 100 = 0`

This behavior is exactly what we need for counting across wrap-arounds!

---

## Files

- **main.py** - Main solution (both parts)
- **part2_solution.py** - Detailed Part 2 implementation with tests
- **debug.py** - Step-by-step debugging for Part 1
- **verify.py** - Manual verification of Part 1 logic
- **analyze_positions.py** - Statistical analysis
- **VERIFICATION_REPORT.md** - Part 1 detailed verification
- **PART2_VERIFICATION.md** - Part 2 detailed verification
- **FINAL_SUMMARY.md** - Part 1 final summary
- **README.md** - This file

---

## Running the Solutions

```bash
# Run both parts
python main.py

# Run part 2 with detailed tests
python part2_solution.py

# Run part 1 with debugging
python debug.py
```

---

## Verification Summary

### Part 1 Verification ✓
- Example: 3 (expected 3) ✓
- Input: 1,165 zeros
- All edge cases tested
- All tests pass

### Part 2 Verification ✓
- Example: 6 (expected 6) ✓
- Input: 6,496 zeros
- 11 test cases all pass
- Mathematical formulas proven
- Edge cases (starting at 0, R1000, etc.) all correct

### Comparison
- Part 2 - Part 1 = 6,496 - 1,165 = 5,331 additional zeros
- Ratio: 6,496 / 1,165 ≈ 5.58
- This makes sense: many large rotations pass through 0 multiple times

---

## Key Insights

1. **Modulo Arithmetic**: Using `% 100` elegantly handles circular wrap-around
2. **Python's Floor Division**: The `//` operator's behavior with negative numbers is perfect for this problem
3. **Counting Multiples**: The formulas count multiples of 100 in specific ranges
4. **Efficiency**: Both solutions run in O(n) time where n is the number of rotations

---

## Confidence Level

**Both Parts**: MAXIMUM ✓✓✓

All verifications pass, mathematical formulas proven, and results are logical and consistent.

**Status**: READY TO SUBMIT ✓✓✓
