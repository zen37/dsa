def find_largest(lst: list):
    """
    Return the largest number in the list.

    Assumes all elements are numbers and the list is non-empty.

    Time: O(n), where n is the length of the list.
    Space: O(1), only a single reference is tracked.
    """
    largest = lst[0]

    for item in lst[1:]:
        if item > largest:
            largest = item

    return largest


def find_largest_index(lst: list) -> int:
    """
    Return the index of the largest number in the list. If the largest
    value appears multiple times, the earliest index is returned.

    Assumes all elements are numbers

    Time: O(n), where n is the length of the list.
    Space: O(1), only the current best index is tracked.
    """
    largest_index: int = 0

    for i in range(1, len(lst)):
        if lst[i] > lst[largest_index]:
            largest_index = i

    return largest_index


if __name__ == "__main__":
    print(find_largest([1, 5, 3, 5, 2]))  # 5
    print(find_largest([-1, -5, -3]))  # -1
    print(find_largest_index([1, 5, 3, 5, 2]))  # 1 (first 5)
    print(find_largest_index([2]))  # 0
