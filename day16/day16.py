import re
import sys
from typing import Callable, Dict, List, Tuple, Union

# Alias comparison functions for readability
equals = lambda a, b: a == b
less_than = lambda a, b: a < b
greater_than = lambda a, b: a > b

GOAL_SUE = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def parse_sue(raw_sue: str, name_prefix="Sue ") -> Tuple[int, Dict[str, int]]:
    """Parse and return your aunt's serial number and attributes as a dict."""
    # Snag the number between your aunt's name and the colon
    serial: str = raw_sue[len(name_prefix) : raw_sue.index(":")]

    # Match key: value pairs
    pattern = re.compile(r"(\w+):\s(\d+)")

    return int(serial), {prop: int(qty) for prop, qty in pattern.findall(raw_sue)}


def find_target_sue(
    sues: List[Tuple[int, Dict[str, int]]],
    target_sue: Dict[str, int],
    rule_functions: Dict[str, Callable] = {},
    default_rule=equals,
) -> Union[int, None]:
    """Return the serial number of the first sue that matches the provided rules."""

    # Test each sue's attributes against our target sue's attributes,
    # using the provided rules, using the default_rule if not provided
    # and return the first matching sue that matches all the rules
    for serial, attributes in sues:
        if all(
            rule_functions.get(prop, default_rule)(attributes[prop], target_sue[prop])
            for prop in attributes.keys()
        ):
            return serial

    # make mypy happy
    return None


def main():
    assert parse_sue("Sue 10: akitas: 7, trees: 8, pomeranians: 4") == (
        10,
        {"akitas": 7, "trees": 8, "pomeranians": 4},
    )

    filename: str = sys.argv[1]
    sues: List[Tuple[int, Dict[str, int]]] = [
        parse_sue(raw_sue) for raw_sue in open(filename).readlines()
    ]

    p1_sue_id: Union[int, None] = find_target_sue(sues, GOAL_SUE)
    print(f"Part 1 sue ID: {p1_sue_id}")

    part_2_rules: Dict[str, Callable] = {
        "cats": greater_than,
        "trees": greater_than,
        "pomeranians": less_than,
        "goldfish": less_than,
    }

    p2_sue_id: Union[int, None] = find_target_sue(sues, GOAL_SUE, part_2_rules)
    print(f"Part 2 sue ID: {p2_sue_id}")


if __name__ == "__main__":
    main()
