import sys
from itertools import combinations
from typing import List, Sequence, Tuple


def ways_to_fill(sizes: Sequence[int], amount: int) -> Tuple[Tuple[int, ...], ...]:
    """Return a tuple of tuples with each different way to make the given amount."""
    return tuple(
        tuple(combo)
        for r in range(1, len(sizes))
        for combo in combinations(sizes, r)
        if sum(combo) == amount
    )


def main():
    filename: str = sys.argv[1]
    raw_lines: List[str] = open(filename).readlines()

    amount: int = int(raw_lines[0])
    sizes: Tuple[int, ...] = tuple(int(line) for line in raw_lines[1:])

    ways_to: Tuple[Tuple[int, ...], ...] = ways_to_fill(sizes, amount)
    print(f"Part 1 ways to make {amount}: {len(ways_to)}")

    # Not the fastest since we're iterating over ways_to twice, but readable.
    fewest_containers: int = min(len(combo) for combo in ways_to)
    efficient_ways_to: Tuple[Tuple[int, ...], ...] = tuple(
        combo for combo in ways_to if len(combo) == fewest_containers
    )
    print(
        f"Part 2 ways to make {amount} in {fewest_containers} the fewest containers: {len(efficient_ways_to)}"
    )


if __name__ == "__main__":
    main()
