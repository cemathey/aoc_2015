import sys
from typing import NamedTuple, List, Tuple, Iterator
from itertools import combinations, repeat
from functools import reduce
from pprint import pprint


class Package(NamedTuple):
    length: int
    width: int
    height: int


def package_surfaces(package: Package) -> Iterator[Tuple[int, int]]:
    """Yield a pair of dimensions for each pair of dimensions, l,w l,h, w,h"""
    for dimension_pair in combinations(package, 2):
        yield dimension_pair


def parse_package(raw_package: str, seperator="x") -> Package:
    """Return a Package of the given dimensions."""

    # Tuple unpack to raise an exception if anything besides a 3 dimensional package is provided
    length, width, height = map(int, raw_package.split(seperator))

    return Package(length, width, height)


def parse_packages(raw_packages: List[str]) -> Iterator[Package]:
    """Yield a Package for each string of package dimensions, i.e. 2x3x4"""
    for raw_package in raw_packages:
        yield parse_package(raw_package)


def calc_required_ribbon(package: Package) -> int:
    """Return the total ribbon required, the cubic volume of the package + the shortest distance around the sides."""

    # Bow
    cubic_volume = reduce(lambda total, side: total * side, package, 1)

    # The smallest two dimensions for the package ribbon
    shortest_distance = sum(package) - max(package)

    # Double the shortest distance for the mirror faces
    return cubic_volume + shortest_distance * 2


def calc_required_paper(package: Package) -> int:
    """Return the amount of wrapping paper for a single package.

    return: surface area + area of smallest side
    """
    side_areas: Tuple[int, ...] = tuple(
        dim1 * dim2 for dim1, dim2 in package_surfaces(package)
    )
    surface_areas: Tuple[int, ...] = tuple(2 * area for area in side_areas)

    return sum(surface_areas) + min(side_areas)


def main():
    filename: str = sys.argv[1]
    raw_packages: List[str] = open(filename).readlines()
    packages = tuple(parse_packages(raw_packages))

    assert calc_required_paper(Package(2, 3, 4)) == 58
    assert calc_required_paper(Package(1, 1, 10)) == 43
    assert calc_required_ribbon(Package(2, 3, 4)) == 34
    assert calc_required_ribbon(Package(1, 1, 10)) == 14

    total_area = sum(calc_required_paper(package) for package in packages)
    print(f"Total paper: {total_area}")

    total_ribbon = sum(calc_required_ribbon(package) for package in packages)
    print(f"Total ribbon: {total_ribbon}")


if __name__ == "__main__":
    main()