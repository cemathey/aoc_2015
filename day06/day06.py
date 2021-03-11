import re
import sys
from collections import defaultdict
from os import sep
from typing import Callable, DefaultDict, Iterator, List, NamedTuple, Sequence, Tuple
from functools import reduce

# Include state arg even when not used to simplify calling
OPERATIONS = {
    "toggle": lambda state: not state,
    "turn on": lambda state: True,
    "turn off": lambda state: False,
}


class GridSize(NamedTuple):
    minimum: int = 0
    maximum: int = 999_999


GRID_SIZE = GridSize()


class Instruction(NamedTuple):
    operation: str
    start_x: int
    start_y: int
    stop_x: int
    stop_y: int


def parse_instruction(raw_instruction: str, point_seperator=",") -> Instruction:
    """Parse an instruction i.e. 'turn off 446,432 through 458,648' and return a properly formed Instruction NamedTuple"""
    left, stop_point = raw_instruction.split(" through ")
    operation, start_point = re.match(r"^([a-z ]+)\s([\d,]+)", left).groups()

    if operation not in OPERATIONS.keys():
        raise ValueError(f"Invalid operation: {operation}")

    start_x, start_y = start_point.split(point_seperator)
    stop_x, stop_y = stop_point.split(point_seperator)

    return Instruction(operation, int(start_x), int(start_y), int(stop_x), int(stop_y))


def parse_instructions(raw_instructions: List[str]) -> Iterator:
    """Yield an Instruction NamedTuple for each raw instruction."""
    for instruction in raw_instructions:
        yield parse_instruction(instruction)


def generate_coordinates(
    start_point: Tuple[int, int], stop_point: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Generate the x,y coordinates for every point that falls between our starting/ending coordinate pairs."""

    start_x, start_y = start_point
    stop_x, stop_y = stop_point

    if (
        start_x < GRID_SIZE.minimum
        or start_y < GRID_SIZE.minimum
        or stop_x > GRID_SIZE.maximum
        or stop_y > GRID_SIZE.maximum
    ):
        raise ValueError(f"{start_point} to {stop_point} exceeds {GRID_SIZE} limit.")

    for x in range(start_x, stop_x + 1):
        for y in range(start_y, stop_y + 1):
            yield (x, y)


def process_instructions(
    instructions: Sequence[Instruction],
) -> DefaultDict[Tuple[int, int], bool]:
    """Update the state of every affected point for each instruction and return the state."""
    lights_state: DefaultDict[Tuple[int, int], bool] = defaultdict(bool)

    for instruction in instructions:
        for point in generate_coordinates(
            (instruction.start_x, instruction.start_y),
            (instruction.stop_x, instruction.stop_y),
        ):
            state: bool = lights_state[point]

            # Snag the update function for this type of operation and update our point's state
            operation: Callable = OPERATIONS[instruction.operation]
            lights_state[point] = operation(state)

    return lights_state


def main():
    filename: str = sys.argv[1]
    raw_instructions: List[str] = open(filename).readlines()

    instructions: Tuple[Instruction, ...] = tuple(parse_instructions(raw_instructions))

    lights_state: DefaultDict[Tuple[int, int], bool] = process_instructions(
        instructions
    )

    turned_on_lights: int = reduce(
        lambda total, state: total + (1 if state else 0), lights_state.values(), 0
    )

    print(f"Part 1 turned on lights: {turned_on_lights}")


if __name__ == "__main__":
    main()
