import json
import sys


def recursive_sum(element, forbidden_value="red") -> int:
    """Recurse through the parsed JSON data until we hit integer primitives.

    forbidden_value: Skip dictionaries and any children containing this value.
    """
    total: int = 0

    for sub_element in element:
        if isinstance(sub_element, dict):
            if forbidden_value not in sub_element.values():
                total += recursive_sum(sub_element.items(), forbidden_value)
        elif isinstance(sub_element, list):
            total += recursive_sum(sub_element, forbidden_value)
        elif isinstance(sub_element, tuple):
            total += recursive_sum(sub_element, forbidden_value)
        elif isinstance(sub_element, int):
            total += sub_element

    return total


def main():
    filename = sys.argv[1]
    data = json.load(open(filename))

    # Use a guaranteed to be unique sentinel
    total = recursive_sum(data, forbidden_value=object())
    print(f"Part 1 total: {total}")

    total = recursive_sum(data)
    print(f"Part 2 total: {total}")


if __name__ == "__main__":
    main()