def unique_elements(lst: list) -> list:
    """
    Return items that appear exactly once in the input list,
    in their order of first appearance.

    Time: O(n), where n is the length of the input list.
    Space: O(n) for the count table and the result list.
    """
    counts: dict = {}

    for item in lst:
        counts[item] = counts.get(item, 0) + 1

    result: list = []

    # Dicts preserve insertion order in Python 3.7+
    # so iterating `counts` gives us items in first-appearance order for free.
    #
    # On older Python versions, dict ordering is not guaranteed, so we would need to
    # iterate the original list instead to preserve order:
    #
    #     for item in lst:
    #         if counts[item] == 1:
    #             result.append(item)

    for item, count in counts.items():
        if count == 1:
            result.append(item)

    return result


if __name__ == "__main__":
    print(unique_elements([1, 2, 2, 3, 4, 4, 5]))  # returns [1, 3, 5]
    print(unique_elements([1, 2, 2, 3, "", " ", 4, 4, 5]))
    print(unique_elements([1, 2, "a", 2, 3, "", " ", 4, "a", "c ", "a ", 5]))
