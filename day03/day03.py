import sys
from typing import List, Tuple, Iterable, Set, Optional


def find_visited_houses(
    directions: Iterable[str],
    x: int = 0,
    y: int = 0,
    east=">",
    west="<",
    north="^",
    south="v",
    visited: Optional[Set] = None,  # type: ignore
):
    """Return the number of houses visited at least once for each step in directions."""

    # Allow passing initialized visited to handle santa/robot santa
    if visited is None:
        visited: Set[Tuple[int, int]] = set()  # type: ignore

    assert visited is not None  # Mypy complains about methods acting on None

    # Visit the starting house
    visited.add((x, y))

    for direction in directions:
        if direction not in (east, west, north, south):
            raise ValueError(f"Invalid direction: {direction}")

        if direction == north:
            y += 1
        elif direction == east:
            x += 1
        elif direction == west:
            x -= 1
        elif direction == south:
            y -= 1

        visited.add((x, y))

    return len(visited)


def visit_with_robot_santa(directions: List[str]) -> int:
    """Have santa/robot santa visit each house and return the combined number of visited houses."""
    santa_directions: List[str] = directions[0::2]
    robot_directions: List[str] = directions[1::2]
    visited: Set[Tuple[int, int]] = set()

    # We don't care about the number of houses after only Santa has visited
    _ = find_visited_houses(santa_directions, visited=visited)
    number_houses_visited: int = find_visited_houses(robot_directions, visited=visited)

    return number_houses_visited


def main():
    filename: str = sys.argv[1]
    directions: List[str] = list(open(filename).read())

    assert find_visited_houses(list(">")) == 2
    assert find_visited_houses(list("^>v<")) == 4
    assert find_visited_houses(list("^v^v^v^v^v")) == 2

    visited_houses = find_visited_houses(directions)
    print(f"Part 1 visited houses: {visited_houses}")

    assert visit_with_robot_santa(list("^v")) == 3
    assert visit_with_robot_santa(list("^>v<")) == 3
    assert visit_with_robot_santa(list("^v^v^v^v^v")) == 11

    visited_houses_p2 = visit_with_robot_santa(directions)
    print(f"Part 2 visited houses: {visited_houses_p2}")


if __name__ == "__main__":
    main()