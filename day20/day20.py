from collections import defaultdict
from typing import Iterator, Dict, Tuple, Iterator
from itertools import count
from functools import reduce


def factors(num: int) -> Iterator[int]:
    """Generate all divisors of num"""

    # Should have done up to the square root of the number and
    # yield the divisor and num // divisor
    for divisor in range(1, (num // 2) + 1):
        if num % divisor == 0:
            yield divisor

    yield num


def lowest_house_number(stop_at, present_factor=10, house_limit=None) -> int:
    """ """
    used_facs: Dict[int, int] = defaultdict(int)

    for house_num in count(1):
        house_factors: Iterator[int] = factors(house_num)
        usable_factors: Iterator[int]

        if house_limit:
            usable_factors = filter(
                lambda fac: used_facs[fac] <= house_limit, house_factors
            )
        else:
            usable_factors = house_factors

        delivered_presents = reduce(
            lambda total, fac: total + fac * present_factor, usable_factors, 0
        )

        if delivered_presents >= stop_at:
            return house_num

        for fac in house_factors:
            used_facs[fac] += 1

    return 0


def main():
    puzzle_input = 29000000

    house_num = lowest_house_number(puzzle_input)
    print(f"Part 1 house number: {house_num}")

    house_num = lowest_house_number(puzzle_input, present_factor=11, house_limit=50)
    print(f"Part 2 house number: {house_num}")


if __name__ == "__main__":
    main()