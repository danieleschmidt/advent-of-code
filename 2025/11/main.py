from functools import cache

# Global graph for caching
graph = {}


def parse_input(input_file='input.txt'):
    """Parse the input to build a directed graph."""
    global graph
    graph = {}

    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                src, dests = line.split(': ')
                graph[src] = dests.split()


@cache
def count_paths(node):
    """Count all paths from node to 'out'."""
    if node == 'out':
        return 1

    if node not in graph:
        return 0

    return sum(count_paths(n) for n in graph[node])


@cache
def count_paths_with_required(node, visited_mask):
    """Count paths from node to 'out' that visit both 'dac' and 'fft'.

    Bitmask: 0=none, 1=dac, 2=fft, 3=both
    """
    # Update bitmask when visiting required nodes
    if node == 'dac':
        visited_mask |= 1
    if node == 'fft':
        visited_mask |= 2

    if node == 'out':
        # Return 1 only if we've visited both required nodes
        return 1 if visited_mask == 3 else 0

    if node not in graph:
        return 0

    return sum(count_paths_with_required(n, visited_mask) for n in graph[node])


def solve(input_file='input.txt'):
    """Count all paths from 'you' to 'out'."""
    parse_input(input_file)
    count_paths.cache_clear()  # Clear cache for new graph
    return count_paths('you')


def solve_part2(input_file='input.txt'):
    """Count paths from 'svr' to 'out' that visit both 'dac' and 'fft'."""
    parse_input(input_file)
    count_paths_with_required.cache_clear()  # Clear cache for new graph
    return count_paths_with_required('svr', 0)


def main():
    result1 = solve()
    print(f"Part 1 - Paths from you to out: {result1}")

    result2 = solve_part2()
    print(f"Part 2 - Paths from svr to out via dac and fft: {result2}")


if __name__ == "__main__":
    main()
