def sorted_squares(nums: list[int]) -> list[int]:

    # Time O(n); Space O(n)

    if len(nums) == 1:
        return [nums[0] * nums[0]]

    # If the first number is positive, then all the numbers are positive,
    # so we can just return the squares of the numbers.
    # no need for extra work
    if nums[0] >= 0:
        return [num * num for num in nums]

    left_pos: int = 0
    right_pos: int = len(nums) - 1

    insert_pos: int = len(nums) - 1

    left: int = nums[left_pos]
    right: int = nums[right_pos]

    left_square: int = 0
    right_square: int = 0

    nums_square = [0] * len(nums)

    while left < right:
        left = nums[left_pos]
        right = nums[right_pos]

        left_square = left * left
        right_square = right * right

        if left_square >= right_square:
            nums_square[insert_pos] = left_square
            left_pos += 1
        else:
            nums_square[insert_pos] = right_square
            right_pos -= 1

        insert_pos -= 1

    return nums_square


if __name__ == "__main__":
    print(sorted_squares([-4, -1, 0, 3, 10]))
    print(sorted_squares([-7, -3, 2, 3, 11, 15]))
    print(sorted_squares([-5, -3, -2, -1]))
    print(sorted_squares([-2, -2, 2, 2]))
    print(sorted_squares([-1, -1, 0, 1, 1]))
    print(sorted_squares([-7, -3, 2, 3, 11]))
