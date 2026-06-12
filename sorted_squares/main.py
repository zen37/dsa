def sorted_squares(nums: list[int]) -> list[int]:
    """
    Return a sorted list of the squares of a sorted input list.

    Uses a two-pointer approach to achieve O(n) time, exploiting the fact that
    the input is already sorted: the largest square must come from one of the
    two ends (the most negative or the most positive value), so we fill the
    output from the back, comparing the squares at each end.

    Args:
        nums: A list of integers sorted in non-decreasing order.

    Returns:
        A new list containing the squares of each element, sorted in
        non-decreasing order.

    Time:  O(n) - each element is visited exactly once.
    Space: O(n) - the output list; no other space scales with input.

    Examples:
        >>> sorted_squares([-4, -1, 0, 3, 10])
        [0, 1, 9, 16, 100]
        >>> sorted_squares([-7, -3, 2, 3, 11])
        [4, 9, 9, 49, 121]
    """
    # Time: O(n); Space: O(n)
    if len(nums) == 1:
        return [nums[0] * nums[0]]

    # Fast path: if the smallest value is non-negative, the whole list is
    # non-negative and already sorted, so squaring preserves order.
    if nums[0] >= 0:
        return [num * num for num in nums]

    left_pos: int = 0
    right_pos: int = len(nums) - 1
    insert_pos: int = len(nums) - 1
    nums_square: list[int] = [0] * len(nums)

    while left_pos <= right_pos:
        left_square = nums[left_pos] * nums[left_pos]
        right_square = nums[right_pos] * nums[right_pos]

        if left_square >= right_square:
            nums_square[insert_pos] = left_square
            left_pos += 1
        else:
            nums_square[insert_pos] = right_square
            right_pos -= 1
        insert_pos -= 1

    return nums_square
