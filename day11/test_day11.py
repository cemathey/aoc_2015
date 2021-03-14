from day11 import (
    increment_password,
    no_invalid_letters,
    has_valid_letter_pairs,
    is_valid_length,
    has_valid_char_run,
)


def test_lazy_testing():

    assert increment_password("xx") == "xy"
    assert increment_password("xy") == "xz"
    assert increment_password("xz") == "ya"
    assert increment_password("ya") == "yb"
    assert increment_password("yb") == "yc"

    assert not no_invalid_letters("some")
    assert not no_invalid_letters("leer")
    assert not no_invalid_letters("wingo")
    assert no_invalid_letters("yay")

    assert has_valid_letter_pairs("aagreatzz")
    assert has_valid_letter_pairs("aazzbbxx")
    assert not has_valid_letter_pairs("abzcdd")
    assert not has_valid_letter_pairs("aabcbcbc")

    assert has_valid_char_run("hijklmmn")
    assert not has_valid_char_run("acd")

    assert is_valid_length("abcdffaa")
    assert no_invalid_letters("abcdffaa")
    assert has_valid_letter_pairs("abcdffaa")
    assert has_valid_char_run("abcdffaa")
