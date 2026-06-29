def check_distance_duplicates(nums: list[int], k: int) -> bool:

    if len(nums) < 2:
        return False
    if k == 0:
        return False
    if k >= len(nums) - 1:
        return len(nums) != len(set(nums))

    nums_dict: dict[int, int] = {}

    for i, num in enumerate(nums):
        if num in nums_dict:
            if i - nums_dict[num] <= k:
                return True
            else:
                nums_dict[num] = i
        else:
            nums_dict[num] = i

    return False
