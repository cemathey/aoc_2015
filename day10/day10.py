from itertools import groupby
from typing import List
import sys


def look_say(sequence: str) -> str:
    """Generate the next sequence."""
    new_sequence: List[str] = []

    for char, group in groupby(sequence):
        new_sequence.append(str(len(tuple(group))))
        new_sequence.append(char)

    return "".join(new_sequence)


def look_say_n_times(sequence: str, times: int) -> str:
    """Perform look and say n times."""
    for _ in range(times):
        sequence = look_say(sequence)

    return sequence


def main():
    filename: str = sys.argv[1]
    sequence: str = open(filename).read().strip()

    assert look_say_n_times("1", 5) == "312211"

    part_1: int = len(look_say_n_times(sequence, 40))
    print(f"Part 1: {part_1}")

    part_2: int = len(look_say_n_times(sequence, 50))
    print(f"Part 2: {part_2}")


if __name__ == "__main__":
    main()