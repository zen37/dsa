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

    # Time: first loop - O(n); second loop - O(n) x O(n) x O(n) = O(n^3) -> O(n) + O(n³) = O(n³)
    # Space:  O(n)

    if len(nums) == 2:
        return [0, 1]

    nums_dict: dict[int:int] = {}

    for i, num in enumerate(nums):
        nums_dict[num] = nums_dict.get(num, []) + [i]

    for i, num in enumerate(nums):
        for key in nums_dict:
            if (num + key) == target:
                for idx in nums_dict[key]:
                    if idx != i:  # make sure we don't use same index twice
                        return [i, idx]


if __name__ == "__main__":
    print(two_sum([1, 3, 3], 6))
