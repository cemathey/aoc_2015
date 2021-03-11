import re
import sys
from collections import defaultdict
from functools import reduce
from typing import Callable, DefaultDict, Iterator, List, NamedTuple, Sequence, Tuple

# Part 1
# toggle: invert state
# turn on: turn on
# turn off: turn off
# Include state arg even when not used to simplify calling
PART_1_OPERATIONS = {
    "toggle": lambda state: 0 if state >= 1 else 1,
    "turn on": lambda state: 1,
    "turn off": lambda state: 0,
}

# Part 2:
# toggle: increase brightness by 2
# turn on: increase brightness by
# turn off: decrease brightness by 1 min 0
PART_2_OPERATIONS = {
    "toggle": lambda brightness: brightness + 2,
    "turn on": lambda brightness: brightness + 1,
    "turn off": lambda brightness: brightness + (-1 if brightness >= 1 else 0),
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

    if operation not in PART_1_OPERATIONS.keys():
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
    instructions: Sequence[Instruction], part_1
) -> DefaultDict[Tuple[int, int], int]:
    """Update the state of every affected point for each instruction and return the state."""
    lights_state: DefaultDict[Tuple[int, int], int] = defaultdict(int)

    for instruction in instructions:
        for point in generate_coordinates(
            (instruction.start_x, instruction.start_y),
            (instruction.stop_x, instruction.stop_y),
        ):
            state: int = lights_state[point]

            # Snag the update function for this type of operation and update our point's state
            if part_1:
                operations_lookup = PART_1_OPERATIONS
            else:
                operations_lookup = PART_2_OPERATIONS

            operation: Callable = operations_lookup[instruction.operation]
            lights_state[point] = operation(state)

    return lights_state


def main():
    filename: str = sys.argv[1]
    raw_instructions: List[str] = open(filename).readlines()

    instructions: Tuple[Instruction, ...] = tuple(parse_instructions(raw_instructions))

    lights_state: DefaultDict[Tuple[int, int], int] = process_instructions(
        instructions, part_1=True
    )

    # Count the number of turned on lights
    turned_on_lights: int = reduce(
        lambda total, state: total + (1 if state > 0 else 0),
        lights_state.values(),
        0,
    )

    print(f"Part 1 turned on lights: {turned_on_lights}")

    lights_brightness: DefaultDict[Tuple[int, int], int] = process_instructions(
        instructions, part_1=False
    )

    # Sum the total brightness
    total_brightness: int = sum(lights_brightness.values())
    print(f"Part 2 total brightness: {total_brightness}")


if __name__ == "__main__":
    main()
