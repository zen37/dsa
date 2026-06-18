def missing_number(nums: list[int]) -> int:
    """Return the one value in [0, n] absent from nums.

    nums holds n distinct integers drawn from the range [0, n] (so its length
    is n and exactly one value in that range is missing). The sum of the full
    range 0..n is n * (n + 1) // 2 by Gauss's formula; subtracting the actual
    sum of nums leaves the missing value.

    Constraints:
        - nums contains distinct integers from [0, n].
        - len(nums) == n; exactly one value in [0, n] is absent.

    Args:
        nums: The list of distinct integers.

    Returns:
        The missing integer.

    Complexity:
        n = len(nums).
        Time:  O(n) - one pass to sum nums.
        Space: O(1) - only running totals; no scaling allocation.
    """
    n: int = len(nums)
    expected_sum: int = n * (n + 1) // 2
    return expected_sum - sum(nums)
