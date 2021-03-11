import pytest

from day06 import generate_coordinates, parse_instruction, Instruction


@pytest.mark.parametrize(
    "instruction, expected",
    [
        ("toggle 296,687 through 906,775", Instruction("toggle", 296, 687, 906, 775)),
        ("turn on 715,871 through 722,890", Instruction("turn on", 715, 871, 722, 890)),
        ("turn off 50,197 through 733,656", Instruction("turn off", 50, 197, 733, 656)),
    ],
)
def test_parse_instruction(instruction, expected):
    assert parse_instruction(instruction) == expected


@pytest.mark.parametrize(
    "instruction, expectation",
    [("not a real instruction 12,384 through 43,583", pytest.raises(ValueError))],
)
def test_parse_instruction_exceptions(instruction, expectation):
    with expectation:
        parse_instruction(instruction)