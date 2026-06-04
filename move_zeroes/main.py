def move_zeros(nums: list[int]) -> list[int]:
    """Move all zeros in the list to the end while maintaining the order of non-zero elements."""
    # Time: O(n), Space: O(1)

    insert_pos = 0

    for i, num in enumerate(nums):
        if num != 0:
            nums[insert_pos], nums[i] = nums[i], nums[insert_pos]
            insert_pos += 1

    return nums


if __name__ == "__main__":
    print(move_zeros([0, 0, 1, 2, 3]))
