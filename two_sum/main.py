def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Given a list of integers and a target integer, return the indices of the two numbers that add up to the target.
    Assume exactly one valid answer exists, and you may not use the same element twice.

    Constraints:
        2 <= len(nums) <= 10^4
        -10^9 <= nums[i] <= 10^9
        -10^9 <= target <= 10^9
        Exactly one valid answer exists.
        You may not use the same index twice.
        All inputs are integers.
    """

    # Time: O(n)
    # Space: O(n)

    nums_dict: dict[int, int] = {}

    for i, num in enumerate(nums):
        difference = target - num
        if difference in nums_dict:
            return [nums_dict[difference], i]  # [smaller_index, larger_index]
        nums_dict[num] = i


if __name__ == "__main__":
    print(two_sum([1, 5, 3, 7], 8))
