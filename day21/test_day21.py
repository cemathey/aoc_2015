import pytest

from day21 import Character, calc_damage, fight_battle, parse_character_stat


@pytest.mark.parametrize(
    "player, boss, expected",
    [
        (Character("player", 8, 5, 5), Character("boss", 12, 7, 2), 3),
        (Character("boss", 12, 7, 2), Character("player", 8, 5, 5), 2),
    ],
)
def test_calc_damage(player, boss, expected):
    assert calc_damage(player, boss) == expected


@pytest.mark.parametrize(
    "player, boss, expected",
    [
        (Character("player", 8, 5, 5), Character("boss", 12, 7, 2), "player"),
        (Character("boss", 12, 7, 2), Character("player", 8, 5, 5), "boss"),
    ],
)
def test_fight_battle(player, boss, expected):
    winner = fight_battle(player, boss)
    assert winner.name == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [("Hit Points: 12\n", 12), ("Damage: 7\n", 7), ("Armor: 2\n", 2)],
)
def test_parse_character_stat(test_input, expected):
    assert parse_character_stat(test_input) == expected