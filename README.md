# Advent of Code

My Advent of Code solutions in Python.

## Structure

```
solutions/
  2024/
    day01/  solution.py  input.txt (not committed)
    day02/  solution.py
    ...
utils/
  aoc.py   — shared utilities (input parsing, grid helpers, etc.)
tests/
  test_utils.py
runner.py  — run a specific day: python runner.py 2024 1
```

## Running

```bash
# Run a specific day
python runner.py 2024 1

# Run all tests
pytest tests/ -v
```

## Notes

Input files are not committed (personal inputs per AoC ToS).
Place your `input.txt` in the relevant `solutions/<year>/day<NN>/` directory.
