def move_zeros(nums: list[int]) -> list[int]:
    """Move all zeros in the list to the end while maintaining the order of non-zero elements."""
    # Time: O(n), Space: O(1)

    insert_pos: int = 0

    for i, num in enumerate(nums):
        if num != 0:
            temp: int = nums[insert_pos]  # i=0, 2; i=2, 0;
            nums[insert_pos] = nums[i]  # 2; nums[1]=nums[2]=1
            # nums[insert_pos], nums[i] = nums[i], nums[insert_pos]
            nums[i] = temp  # i=0, 2; nums[2]=0
            insert_pos += 1  # 1;
            print(nums)
    return nums


if __name__ == "__main__":
    print(move_zeros([2, 0, 1, 17, 3]))
