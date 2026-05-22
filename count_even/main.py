def count_even(lst: list) -> int:
    """
    Return the number of even integers in the list.

    Time: O(n), where n is the length of the list.
    Space: O(1), only a counter is used.
    """
    even_count: int = 0

    for item in lst:
        if (
            isinstance(item, (int, float))
            and not isinstance(item, bool)
            and item % 2 == 0
        ):
            even_count += 1

    return even_count


if __name__ == "__main__":
    print(count_even([2, 1, 2, 3, 4]))  # Expected: 3
    print(count_even([1, 2, 3, 4, 5, 6, 7, 8]))  # Expected: 4
    print(count_even([1, 2, "b", 4, "x", 6, 7, 8]))  # Expected: 4
    print(count_even([2, False, 2, 3, 4]))  # Expected: 3
