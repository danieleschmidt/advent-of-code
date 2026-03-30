import math
from collections import defaultdict


class UnionFind:
    """Union-Find data structure for tracking connected components."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        """Find the root of x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """Union two sets by rank."""
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # Already in the same set

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True

    def get_component_sizes(self):
        """Get the sizes of all connected components."""
        components = defaultdict(int)
        for i in range(len(self.parent)):
            root = self.find(i)
            components[root] += 1
        return list(components.values())

    def num_components(self):
        """Get the number of distinct components."""
        roots = set()
        for i in range(len(self.parent)):
            roots.add(self.find(i))
        return len(roots)


def parse_positions(input_file='input.txt'):
    """Parse the junction box positions from input."""
    positions = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y, z = map(int, line.split(','))
                positions.append((x, y, z))
    return positions


def distance(p1, p2):
    """Calculate Euclidean distance between two 3D points."""
    return math.sqrt((p1[0] - p2[0]) ** 2 +
                     (p1[1] - p2[1]) ** 2 +
                     (p1[2] - p2[2]) ** 2)


def solve(input_file='input.txt', num_connections=1000):
    """Solve Part 1: product of three largest circuit sizes after connections."""
    positions = parse_positions(input_file)
    n = len(positions)

    # Calculate all pairwise distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(positions[i], positions[j])
            distances.append((dist, i, j))

    # Sort by distance
    distances.sort()

    # Create Union-Find structure
    uf = UnionFind(n)

    # Connect the closest num_connections pairs
    connections_made = 0
    for dist, i, j in distances:
        if connections_made >= num_connections:
            break
        uf.union(i, j)
        connections_made += 1

    # Get component sizes
    component_sizes = uf.get_component_sizes()

    # Sort and get the three largest
    component_sizes.sort(reverse=True)

    # Multiply the three largest
    if len(component_sizes) >= 3:
        result = component_sizes[0] * component_sizes[1] * component_sizes[2]
    elif len(component_sizes) == 2:
        result = component_sizes[0] * component_sizes[1]
    elif len(component_sizes) == 1:
        result = component_sizes[0]
    else:
        result = 0

    return result


def solve_part2(input_file='input.txt'):
    """Solve Part 2: product of X coordinates of last connection to unify all."""
    positions = parse_positions(input_file)
    n = len(positions)

    # Calculate all pairwise distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(positions[i], positions[j])
            distances.append((dist, i, j))

    # Sort by distance
    distances.sort()

    # Create Union-Find structure
    uf = UnionFind(n)

    # Connect pairs until all are in one component
    last_i, last_j = None, None
    for dist, i, j in distances:
        if uf.union(i, j):
            last_i, last_j = i, j
            # Check if we have only one component
            if uf.num_components() == 1:
                break

    # Return product of X coordinates
    if last_i is not None and last_j is not None:
        return positions[last_i][0] * positions[last_j][0]
    return 0


def main():
    result1 = solve()
    print(f"Part 1 - Product of three largest circuits: {result1}")

    result2 = solve_part2()
    print(f"Part 2 - Product of X coordinates of final connection: {result2}")


if __name__ == "__main__":
    main()
