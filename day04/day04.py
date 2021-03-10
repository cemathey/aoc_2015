import hashlib
import math
import sys
from itertools import count


def find_hash(goal: str, secret: str, max_steps=math.inf) -> int:
    """Find the lowest positive integer that produces a hash starting with goal, -1 if not found."""
    for step in count(1):
        if step > max_steps:
            break

        hashed = hashlib.md5(f"{secret}{step}".encode("utf-8"))

        if hashed.hexdigest()[0 : len(goal)] == goal:
            return step

    return -1


def main():
    filename: str = sys.argv[1]
    secret: str = open(filename).read()

    goal = "00000"
    assert find_hash(goal, "abcdef") == 609043
    assert find_hash(goal, "pqrstuv") == 1048970

    step: int = find_hash(goal, secret)
    print(f"Part 1 step: {step}")

    goal = "000000"

    step: int = find_hash(goal, secret)
    print(f"Part 2 step: {step}")


if __name__ == "__main__":
    main()
