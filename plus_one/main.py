def plus_one(digits: list[int]) -> list[int]:
    # Time O(n); Space O(n)  worst case for the carry insert
    add: int = 0
    for i in range(len(digits) - 1, -1, -1):
        if i == len(digits) - 1:
            if digits[i] < 9:
                digits[i] = digits[i] + 1
            else:
                digits[i] = 0
                add = 1
        else:
            if digits[i] < 9:
                digits[i] = digits[i] + add
                add = 0
            elif add != 0:
                digits[i] = 0
                add = 1
    if add == 1:
        digits.insert(0, 1)

    return digits


def plus_one_2(digits: list[int]) -> list[int]:
    # Time: O(n); Space: O(n) worst case for the carry insert
    add: int = 1  # the "+1" we're adding
    for i in range(len(digits) - 1, -1, -1):
        digits[i] += add
        if digits[i] < 10:
            add = 0
            break  # no more carry, stop early
        digits[i] = 0
        add = 1
    if add == 1:
        digits.insert(0, 1)
    return digits


if __name__ == "__main__":
    print(plus_one([1, 2, 3]))
    print(plus_one([9, 9, 9]))
    print(plus_one([1, 9, 5]))
    print(plus_one([0]))
    print(plus_one([1, 9]))
    print("-----------------")
    print(plus_one_2([1, 2, 3]))
    print(plus_one_2([9, 9, 9]))
    print(plus_one_2([1, 9, 5]))
