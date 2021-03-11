from typing import List
import sys
import re


def is_word_nice(word: str) -> bool:
    """Return whether the given word meets the criteria for 'nice'."""
    must_match = (r"[aeiou]{1,}.*[aeiou]{1,}.*[aeiou]{1,}", r"([a-z])\1")
    cant_match = r"ab|cd|pq|xy"

    return (
        all(re.search(pattern, word) is not None for pattern in must_match)
        and re.search(cant_match, word) is None
    )


def is_word_nice_part2(word: str) -> bool:
    must_match = (r"([a-z][a-z]).*\1", r"([a-z])[^\1]\1")

    return all(re.search(pattern, word) is not None for pattern in must_match)


def main():
    filename: str = sys.argv[1]
    words: List[str] = open(filename).readlines()

    nice: int = sum(1 for word in words if is_word_nice(word))
    print(f"Part 1 nice word count: {nice}")

    assert is_word_nice("ugknbfddgicrmopn")
    assert is_word_nice("aaa")
    assert not is_word_nice("jchzalrnumimnmhp")
    assert not is_word_nice("haegwjzuvuyypxyu")
    assert not is_word_nice("dvszwmarrgswjxmb")

    nice: int = sum(1 for word in words if is_word_nice_part2(word))
    print(f"Part 2 nice word count: {nice}")

    assert is_word_nice_part2("qjhvhtzxzqqjkmpb")
    assert is_word_nice_part2("xxyxx")
    assert not is_word_nice_part2("uurcxstgmygtbstg")
    assert not is_word_nice_part2("ieodomkazucvgmuy")


if __name__ == "__main__":
    main()