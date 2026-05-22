def intersection(a: list, b: list) -> list:
    """
    Return elements appearing in both a and b, deduplicated,
    in the order they first appear in a.

    Time: O(n + m), where n = len(a), m = len(b).
    Space: O(n + m) for the lookup set, the seen set, and the result.
    """
    b_set: set = set(b)
    seen: set = set()
    result: list = []

    for item in a:
        if item in b_set and item not in seen:
            result.append(item)
            seen.add(item)

    return result


if __name__ == "__main__":
    print(intersection([1, 2, 3], [2, 3, 4]))  # [2, 3]
    print(intersection([1, 2, 2, 3], [2, 3, 4]))  # [2, 3]
    print(
        intersection(
            ["apple", "banana", "banana", "banana", "cherry"], ["cherry", "grapes"]
        )
    )  # []
