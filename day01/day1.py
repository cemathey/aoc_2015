import sys


# Part 1
def calc_floor(instructions: str, up: str = "(", down: str = ")"):
    """Return the floor number the given instructions take you to"""
    up_count: int = instructions.count(up)
    down_count: int = instructions.count(down)

    return up_count - down_count


# Part 2
def determine_position(
    instructions: str,
    destination: int = -1,
    position: int = 0,
    up: str = "(",
    down: str = ")",
):
    """Return the index of the first instruction that takes you to destination, raises ValueError if not possible"""

    idx: int = 1
    for idx, direction in enumerate(instructions):
        if direction == up:
            position += 1
        elif direction == down:
            position -= 1
        else:
            raise ValueError(f"Invalid instruction {direction}")

        if position == destination:
            return idx + 1

    raise ValueError(f"Can't reach position {destination} with these instructions.")


def main():
    filename: str = sys.argv[1]
    instructions: str = open(filename).read()

    assert calc_floor("(())") == 0
    assert calc_floor("()()") == 0
    assert calc_floor("(((") == 3
    assert calc_floor("(()(()(") == 3
    assert calc_floor("))(((((") == 3
    assert calc_floor("())") == -1
    assert calc_floor("))(") == -1
    assert calc_floor(")))") == -3
    assert calc_floor(")())())") == -3

    destination: int = calc_floor(instructions)
    print(f"floor: {destination}")

    assert determine_position(")") == 1
    assert determine_position("()())") == 5

    position: int = determine_position(instructions)
    print(f"position: {position}")


if __name__ == "__main__":
    main()