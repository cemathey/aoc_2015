from os import read
import sys
from typing import Tuple, Dict, List, Iterator, Set
from pprint import pprint
from collections import defaultdict
import re


def read_contents(filename: str) -> List[str]:
    with open(filename) as fd:
        return fd.readlines()


def parse_rule(line: str, delimeter: str = " => ") -> Tuple[str, str]:
    """Return a key, value tuple of the given molecule rule."""
    key, value = line.split(delimeter)
    return key, value


def build_rules_lookup(raw_contents: List[str]) -> Dict[str, List[str]]:
    """Build the molecule transformation rules dictionary."""
    raw_rules: List[str] = []

    # Molecule rules and the starting molecule are separated by a newline
    for line in raw_contents:
        if line == "\n":
            break

        raw_rules.append(line.strip())

    rules = defaultdict(list)
    for raw_rule in raw_rules:
        key, value = parse_rule(raw_rule)
        rules[key].append(value)

    return rules


def tokenize_starting_with(
    rules_lookup: Dict[str, List[str]], starting_with: str
) -> List[str]:
    """Tokenize the starting molecule based on the molecule transformation rules."""
    keys: Set[str] = set(rules_lookup.keys())
    max_token_len: int = max(len(key) for key in keys)
    token: str = ""
    tokens: List[str] = []
    for idx, char in enumerate(starting_with):
        token += char
        end_token: bool = False

        # Check the next n to max_token_len sub strings from our position to find the token end point
        for offset in range(1, max_token_len + 1):
            substr: str = starting_with[idx + 1 : idx + offset + 1]
            if substr in keys:
                end_token = True
                break

        if token in keys or end_token:
            tokens.append(token)
            token = ""
        elif char in keys:
            tokens.append(char)
    else:
        # Grab the ending token (if any)
        if token:
            tokens.append(token)

    return tokens


def generate_molecules(rules: Dict[str, List[str]], tokens: List[str]) -> Set[str]:
    """Return a set of molecules that can be made with the starting molecule/transformation rules."""
    ways: List[List[str]] = []
    for idx, token in enumerate(tokens):
        for way in rules[token]:
            ways.append(list(tokens))
            # Swap out the original token with the new molecule
            ways[-1][idx] = way

    return set("".join(way) for way in ways)


def main() -> None:
    filename: str = sys.argv[1]
    raw_contents: List[str] = read_contents(filename)

    # The starting molecule is always the last line in the file
    starting_with: str = raw_contents[-1]

    rules_lookup: Dict[str, List[str]] = build_rules_lookup(raw_contents)
    tokens: List[str] = tokenize_starting_with(rules_lookup, starting_with)
    ways_to: Set[str] = generate_molecules(rules_lookup, tokens)
    print(f"Part 1 distinct molecules: {len(ways_to)}")


if __name__ == "__main__":
    main()