def single_number_dict(nums: list[int]) -> int:

    # Time: O(n), Space: O(n)

    nums_dict: dict[int, int] = {}

    for num in nums:
        nums_dict[num] = nums_dict.get(num, 0) + 1

    for key in nums_dict.keys():
        if nums_dict[key] == 1:
            return key


def single_number_set(nums: list[int]) -> int:

    # Time: O(n), Space: O(n)

    nums_set: set[int] = set()

    for num in nums:
        if num in nums_set:
            nums_set.remove(num)
        else:
            nums_set.add(num)

    return nums_set.pop()


if __name__ == "__main__":
    print(single_number_dict([2, 2, 1]))  # Output: 1
    print(single_number_dict([4, 1, 2, 1, 2]))  # Output: 4
    print(single_number_dict([1]))  # Output: 1
    print(single_number_dict([3, 3, 7, 7, 10]))  # Output: 10
    print("---------------")
    print(single_number_set([2, 2, 1]))  # Output: 1
    print(single_number_set([4, 1, 2, 1, 2]))  # Output: 4
    print(single_number_set([1]))  # Output: 1
    print(single_number_set([3, 3, 7, 7, 10]))  # Output: 10
