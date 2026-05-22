def most_frequent(lst: list):
    """
    Return the most frequent element in the list. On ties, return the
    element that first appears in the list. Returns None for empty input.

    Time: O(n), where n is the length of the list.
    Space: O(k), where k is the number of unique elements.
    """
    if not lst:
        return None

    counts: dict = {}
    for item in lst:
        counts[item] = counts.get(item, 0) + 1

    max_item = None
    max_count = 0
    for item, count in counts.items():
        if count > max_count:
            max_item = item
            max_count = count

    return max_item


if __name__ == "__main__":
    print(most_frequent([1, 2, 3, 2, 1, 1]))  # returns 1
    print(most_frequent([1, 2, 3, 2, 1]))  # returns 1 (tie: 1 and 2 both appear twice)
    print(most_frequent([]))  # returns None
    print(
        most_frequent([1, 2, 3, 4])
    )  # returns 1 (tie: all appear once, but 1 is first)
    print(
        most_frequent([1, 2, "a", 2, "a", 3, "", " ", 4, "a", "c ", "a ", 5])
    )  # returns "a"
