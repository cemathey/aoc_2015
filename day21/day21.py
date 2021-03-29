import re
import sys
from dataclasses import dataclass
from itertools import combinations
from typing import Iterator, NamedTuple, Tuple


@dataclass
class Character:
    name: str = ""
    hp: int = 0
    damage: int = 0
    armor: int = 0


class Item(NamedTuple):
    name: str
    cost: int
    damage: int
    armor: int


def parse_item(raw_item: str) -> Item:
    """Return an Item from the given raw item string."""
    name, cost, damage, armor = raw_item.split()

    return Item(name, int(cost), int(damage), int(armor))


def parse_character_stat(raw_stat: str) -> int:
    """Parse a character stat from the given string."""
    pattern = r"(\d+)"
    stat = re.search(pattern, raw_stat).group()

    return int(stat)


def calc_damage(attacker: Character, defender: Character, min_damage: int = 1) -> int:
    """Return the amount of damage dealt by the attacker."""
    return max(min_damage, attacker.damage - defender.armor)


def fight_battle(player: Character, boss: Character) -> Character:
    """Return the winner after player and boss fight each other."""
    while player.hp > 0 and boss.hp > 0:
        boss.hp -= calc_damage(player, boss)
        if boss.hp <= 0:
            return player

        player.hp -= calc_damage(boss, player)
        if player.hp <= 0:
            return boss

    # Make mypy happy
    return Character()


def generate_item_combinations(
    weapons, armors, rings
) -> Iterator[Tuple[Item, Item, Item, Item]]:
    """Generate every combination of items a player can use.

    Must include one and only one weapon.
    Armor is optional.
    Between 0 and 2 rings.
    """

    for weapon in weapons:
        for armor in armors:
            for ring_one, ring_two in combinations(rings, 2):
                yield weapon, armor, ring_one, ring_two


def find_desired_outcome(
    base_player_stats: Tuple[int, int, int],
    base_boss_stats: Tuple[int, int, int],
    weapons,
    armors,
    rings,
    character: str = "player",
    key=min,
) -> int:
    """Return the least amount of gold required for the player to beat the boss."""

    outcomes = []
    for item_combination in generate_item_combinations(weapons, armors, rings):
        player = Character("player", *base_player_stats)
        boss = Character("boss", *base_boss_stats)
        total_cost: int = 0
        for item in item_combination:
            total_cost += item.cost
            player.armor += item.armor
            player.damage += item.damage

        winner = fight_battle(player, boss)
        if winner.name == character:
            outcomes.append(total_cost)

    return key(outcomes)


def main():
    item_filename: str = sys.argv[1]
    boss_filename: str = sys.argv[2]

    with open(item_filename) as f:
        raw_weapons, raw_armor, raw_rings = f.read().split("\n\n")

    weapons = [parse_item(raw_item) for raw_item in raw_weapons.split("\n")[1:]]
    armors = [parse_item(raw_item) for raw_item in raw_armor.split("\n")[1:]]
    rings = [parse_item(raw_item) for raw_item in raw_rings.split("\n")[1:]]

    empty_item = Item("", 0, 0, 0)

    # Push two empty rings and an empty armor to handle combos without them
    rings.extend([empty_item, empty_item])
    armors.append(empty_item)

    with open(boss_filename) as f:
        boss_hp, boss_damage, boss_armor = (
            parse_character_stat(stat) for stat in f.readlines()
        )

    base_player_stats = (100, 0, 0)
    base_boss_stats = (boss_hp, boss_damage, boss_armor)

    cost = find_desired_outcome(
        base_player_stats, base_boss_stats, weapons, armors, rings
    )
    print(f"Part 1 cost: {cost}")

    cost = find_desired_outcome(
        base_player_stats, base_boss_stats, weapons, armors, rings, "boss", max
    )
    print(f"Part 2 cost: {cost}")


if __name__ == "__main__":
    main()
