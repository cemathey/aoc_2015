from collections import defaultdict
import enum
from itertools import permutations
import sys
import re
from typing import DefaultDict, NamedTuple, List, Dict, Iterator, Sequence, Tuple


class HappinessRule(NamedTuple):
    person: str
    quantity: int
    neighbor: str


def parse_happiness(
    raw_happiness: str,
    pattern=r"(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+).",
) -> HappinessRule:
    """Parse a happiness rule relationship between two people from the input line and return it."""

    # Tuple unpack to halt if a line is unparseable
    person, direction, quantity, neighbor = re.match(pattern, raw_happiness).groups()

    if direction == "gain":
        sign = 1
    else:
        sign = -1

    return HappinessRule(person, int(quantity) * sign, neighbor)


def build_rules_lookup(contents: List[str]) -> Dict[str, Dict[str, int]]:
    """Build a lookup for each person and their happiness change for each other person."""
    rules: Dict[str, Dict[str, int]] = defaultdict(dict)
    for raw_rule in contents:
        rule: HappinessRule = parse_happiness(raw_rule)
        rules[rule.person][rule.neighbor] = rule.quantity

    return rules


def generate_sitting_permutations(
    rules_lookup: Dict[str, Dict[str, int]]
) -> Iterator[Tuple[str, ...]]:
    """Generate every possible seating arrangement for the given rules."""
    unique_people = rules_lookup.keys()

    for perm in permutations(unique_people):
        yield tuple(perm)


def score_sitting_arrangement(
    arrangement: Sequence[str], rules_lookup: Dict[str, Dict[str, int]]
) -> int:
    """Return the total happiness score for a given seating arrangement."""
    score: int = 0
    last_idx: int = len(arrangement) - 1

    for idx, person in enumerate(arrangement):
        left_idx: int = idx - 1
        right_idx: int = idx + 1

        # Wrap around the left edge
        if left_idx < 0:
            left_idx = last_idx

        # Wrap around the right edge
        if right_idx > last_idx:
            right_idx = 0

        score += rules_lookup[person][arrangement[left_idx]]
        score += rules_lookup[person][arrangement[right_idx]]

    return score


def evaluate_rules(raw_rules: List[str]) -> int:
    """Return the best possible score for the given seating rules."""
    rules_lookup: Dict[str, Dict[str, int]] = build_rules_lookup(raw_rules)

    best_score: int = max(
        score_sitting_arrangement(arrangement, rules_lookup)
        for arrangement in generate_sitting_permutations(rules_lookup)
    )

    return best_score


def main():
    first: str = sys.argv[1]
    second: str = sys.argv[2]
    p1_contents: List[str] = open(first).readlines()
    p2_contents: List[str] = open(second).readlines()

    p1_score = evaluate_rules(p1_contents)
    p2_score = evaluate_rules(p2_contents)

    print(f"Part 1 best score: {p1_score}")
    print(f"Part 2 best score: {p2_score}")


if __name__ == "__main__":
    main()