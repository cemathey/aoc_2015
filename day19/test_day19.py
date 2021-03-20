from os import read
import pytest

from day19 import build_rules_lookup, parse_rule, read_contents


@pytest.mark.parametrize(
    ("value, expected"),
    [
        ("H => HO", ("H", "HO")),
        ("H => OH", ("H", "OH")),
        ("O => HH", ("O", "HH")),
    ],
)
def test_parse_rule(value, expected):
    assert parse_rule(value) == expected


def test_build_rules_lookup():
    raw_contents = read_contents("test_input.txt")

    raw_rules = raw_contents[:-2]
    starting_with = raw_contents[-1]
    assert build_rules_lookup(raw_rules) == {"H": ["HO", "OH"], "O": ["HH"]}
