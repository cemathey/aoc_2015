import string
from itertools import tee
import re

from pprint import pprint
from typing import Sequence, Callable, List, Tuple
import math
import sys


def wrap_char(char: str, high: str = "z") -> Tuple[str, bool]:
    new_char = ord(char) + 1
    wrapped = False

    if new_char > ord(high):
        new_char = ord("a")
        wrapped = True

    return chr(new_char), wrapped


def increment_password(
    password: str,
) -> str:
    """Return the next password, incrementing the last character, wrapping to a from z."""
    new_password: List[str] = []

    wrapped: bool = False
    first_round: bool = True
    for char in reversed(password):
        if wrapped or first_round:
            # Always increment the first time
            first_round = False
            new_char, wrapped = wrap_char(char)
            new_password.append(new_char)
        else:
            new_password.append(char)

    return "".join(reversed(new_password))


def is_valid_length(password, length=8) -> bool:
    """Return whether the password meets the exact length requirement."""
    return len(password) == length


def no_invalid_letters(password, not_allowed=r"[iol]") -> bool:
    """Return whether the password contains any invalid letters."""
    return re.search(not_allowed, password) is None


def has_valid_letter_pairs(
    password, pattern=r".*([a-z])\1.*([a-z])\2", required_groups=2
) -> bool:
    """Return whether the password contains the required number of letter pairs."""
    match = re.match(pattern, password)
    return match and len(match.groups()) >= required_groups  # type: ignore


def has_valid_char_run(password, run_length=3) -> bool:
    """Return whether the password contains a run of characters of the required length."""
    if len(password) < run_length:
        return False

    for idx in range(0, len(password) - run_length):

        chars = list(password[idx : idx + run_length])
        # Get the unicode code points for each character in our slice
        code_points = tuple(map(ord, chars))

        first = code_points[0]

        # For this to be a run each code point should be the value of the first
        # character plus its position in the list
        deltas = tuple(first + offset for offset in range(run_length))

        if code_points == deltas:
            return True

    return False


def is_valid_password(password: str, requirements) -> bool:
    """Return whether the password meets each provided password requirement."""
    return all(func(password, *args, **kwargs) for func, args, kwargs in requirements)


def find_next_valid_password(
    starting_password, requirements, iter_limit=math.inf
) -> str:
    """Increment the starting password until a valid password is found or """

    next_password: str = increment_password(starting_password)
    iteration: int = 0
    while not is_valid_password(next_password, requirements):
        next_password = increment_password(next_password)

        if iteration > iter_limit:
            break

    return next_password


def main():
    filename = sys.argv[1]
    password = open(filename).read().strip()

    # Got fancy in part 1 with the expectation that the password requirements would change.
    requirements = (
        (is_valid_length, (), {}),
        (no_invalid_letters, (), {}),
        (has_valid_char_run, (), {}),
        (has_valid_letter_pairs, (), {}),
    )

    next_password = find_next_valid_password(password, requirements)
    print(f"Part 1 next password: {next_password}")

    next_password = find_next_valid_password(next_password, requirements)
    print(f"Part 2 next password: {next_password}")


if __name__ == "__main__":
    main()