def search_linear(nums: list[int], target) -> int:

    # Time O(n), Space O(1)

    for i, num in enumerate(nums):
        if target == num:
            return i

    return -1


def search_binary(nums: list[int], target) -> int:

    # Time O(log n), Space O(1)

    left: int = 0
    right: int = len(nums) - 1
    mid: int = 0

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def search_built_in(nums: list[int], target) -> int:

    import bisect

    # Time ?, Space O(1)

    index = bisect.bisect_left(nums, target)

    if index < len(nums) and nums[index] == target:
        return index
    else:
        return -1


if __name__ == "__main__":
    print("--- linear search ---")
    print(search_linear([-1, 0, 3, 5, 9, 12], 9))
    print(search_linear([], 10))
    print(search_linear([1, 3, 5, 7, 9], 6))  # -> -1

    print("--- binary search ---")
    print(search_binary([-1, 0, 3, 5, 9, 12], 9))
    print(search_binary([], 10))
    print(search_binary([1, 3, 5, 7, 9], 6))  # -> -1

    print("--- built-in search ---")
    print(search_built_in([-1, 0, 3, 5, 9, 12], 9))
    print(search_built_in([], 10))
    print(search_built_in([1, 3, 5, 7, 9], 6))  # -> -1
