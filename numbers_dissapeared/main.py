def find_disappeared_numbers(nums: list[int]) -> list[int]:
    """Return every value in [1, n] that does not appear in nums.

    nums has length n and each element is in [1, n], but values may repeat,
    so some values in the range are absent. Collecting the present values in a
    set and then checking each value of 1..n against it yields the missing
    ones in ascending order.

    Constraints:
        - len(nums) == n; each element is in [1, n].
        - Values may appear more than once.

    Args:
        nums: The list of integers.

    Returns:
        The sorted list of values in [1, n] absent from nums (empty if none).

    Complexity:
        n = len(nums).
        Time:  O(n) - build the set, then one pass over 1..n.
        Space: O(n) - the set of present values, plus the output.
    """

    result: list[int] = []

    for num in range(1, len(nums) + 1):
        if num not in nums:
            result.append(num)

    return result
