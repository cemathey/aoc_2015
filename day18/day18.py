import sys
from copy import deepcopy
from typing import List, NamedTuple, Callable

ON = "#"
OFF = "."


class Point(NamedTuple):
    """Represents an (x,y) coordinate point for a grid."""

    x: int
    y: int


def generate_neighbor_values(grid: List[List[bool]], point: Point):
    """Yield the value of each neighbor of the given point in the grid."""
    offsets = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    grid_size = len(grid)

    for dx, dy in offsets:
        new_x = point.x + dx
        new_y = point.y + dy

        if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
            yield grid[new_x][new_y]


def count_neighbors(grid: List[List[bool]], point: Point, state=True) -> int:
    """Count every adjacent cell of the given point in grid that is set to state."""
    return sum(1 for value in generate_neighbor_values(grid, point) if value == state)


def calc_new_state(
    state: bool,
    on_neighbors: int,
) -> bool:
    """Keep lights on that have 2 <= n <= 3 neighbors that are on, and off otherwise."""
    new_state = False

    if state and 2 <= on_neighbors <= 3:
        new_state = True
    elif not state and on_neighbors == 3:
        new_state = True

    return new_state


def update_grid(grid: List[List[bool]], exceptions=tuple()):
    """Make one pass through the grid and return a new grid."""
    # Don't mutate the original grid
    new_grid = deepcopy(grid)

    for row_idx, row in enumerate(grid):
        for col_idx, col in enumerate(row):
            if Point(row_idx, col_idx) not in exceptions:
                on_neighbors = count_neighbors(grid, Point(row_idx, col_idx))
                new_grid[row_idx][col_idx] = calc_new_state(col, on_neighbors)

    return new_grid


def animate_grid(grid: List[List[bool]], exceptions=(), rounds=100) -> List[List[bool]]:
    """Make n iterations through the grid and return the new grid state."""
    new_grid = deepcopy(grid)

    for _ in range(rounds):
        new_grid = update_grid(new_grid, exceptions)

    return new_grid


def main():
    filename: str = sys.argv[1]
    raw_grid = [list(line.strip()) for line in open(filename).readlines()]

    grid = []
    for row in raw_grid:
        new_row = [True if col == ON else False for col in row]
        grid.append(new_row)

    part_1_grid = animate_grid(grid)
    part_1_on = sum(1 for row in part_1_grid for col in row if col)
    print(f"Part 1: {part_1_on} light's are on.")

    grid_size = len(grid) - 1
    exceptions = (
        Point(0, 0),
        Point(0, grid_size),
        Point(grid_size, 0),
        Point(grid_size, grid_size),
    )

    for point in exceptions:
        grid[point.x][point.y] = True

    part_2_grid = animate_grid(grid, exceptions)
    part_2_on = sum(1 for row in part_2_grid for col in row if col)
    print(f"Part 2: {part_2_on} light's are on.")


if __name__ == "__main__":
    main()
