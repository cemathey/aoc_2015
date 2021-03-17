import sys
from functools import reduce
from itertools import combinations_with_replacement, permutations
from typing import Dict, Iterator, List, NamedTuple, Sequence, Tuple


class Ingredient(NamedTuple):
    name: str
    properties: Dict[str, int]


def parse_ingredient(raw_ingredient: str) -> Ingredient:
    """Parse a provided ingredient string into an Ingredient NamedTuple."""
    recipe_properties = {}
    recipe_name, properties = raw_ingredient.split(": ")
    for chunk in properties.split(", "):
        prop, value = chunk.split()
        recipe_properties[prop] = int(value)

    return Ingredient(recipe_name, recipe_properties)


def score_recipe(
    portion_sizes: Sequence[int],
    ingredients: Sequence[Ingredient],
    property_filter: Sequence[str],
) -> int:
    """Calculate the recipe score given the portion size of each ingredient."""

    invalid_ingredients = set(property_filter)

    # Alias the built in multiply for readability
    multiply = int.__mul__

    # Filter out any unwanted properties, rely on python 3.7+ dictionary key order preservation
    properties: List[Tuple[int, ...]] = []
    for ingredient in ingredients:
        properties.append(
            tuple(
                value
                for key, value in ingredient.properties.items()
                if key not in invalid_ingredients
            )
        )

    # Join each like property from each ingredient together
    # i.e. all capacity are in one sequence, all flavor in another, etc.
    joined_ingredient_props: Tuple[Tuple[int, ...], ...] = tuple(zip(*properties))

    # Calculate the scores for each ingredient property
    scored_ingredients = []
    for props in joined_ingredient_props:
        # Join each portion size to its property
        joined_portion_sizes = tuple(zip(props, portion_sizes))
        scored_ingredients.append(
            sum(multiply(*items) for items in joined_portion_sizes)
        )

    return reduce(
        lambda total, score: total * (score if score > 0 else 0), scored_ingredients
    )


def count_recipe_calories(
    portion_sizes: Sequence[int],
    ingredients: Sequence[Ingredient],
    calorie_key="calories",
):
    """Return the total calories for the given recipe."""
    return sum(
        portion * ingredient.properties[calorie_key]
        for portion, ingredient in zip(portion_sizes, ingredients)
    )


def get_recipe_portion_combinations(
    ingredients: Sequence[Ingredient],
    recipe_size_limit: int = 100,
) -> Iterator[Tuple[int, ...]]:
    """Generate all the possible ways to add N ingredients together to make our recipe limit."""

    for combo in combinations_with_replacement(
        range(recipe_size_limit + 1), len(ingredients)
    ):
        # Restrict any invalid recipe sizes since we'll be generating permutations
        # which will dramatically increase the search space
        if sum(combo) == recipe_size_limit:
            yield combo


def main():
    filename: str = sys.argv[1]
    ingredients: Tuple[Ingredient, ...] = tuple(
        parse_ingredient(raw_ingredient)
        for raw_ingredient in open(filename).readlines()
    )

    recipe_portion_permutations = tuple(
        permutation
        for ways_to_recipe_limit in get_recipe_portion_combinations(ingredients)
        for permutation in permutations(ways_to_recipe_limit)
    )

    invalid_properties: Sequence[str] = ("calories",)

    highest_score: int = max(
        score_recipe(portion_permutation, ingredients, invalid_properties)
        for portion_permutation in recipe_portion_permutations
    )

    print(f"Part 1 highest score: {highest_score}")

    highest_500_cal_score: int = max(
        score_recipe(portion_permutation, ingredients, invalid_properties)
        for portion_permutation in recipe_portion_permutations
        if count_recipe_calories(portion_permutation, ingredients) == 500
    )

    print(f"Part 2 highest score: {highest_500_cal_score}")


if __name__ == "__main__":
    main()
