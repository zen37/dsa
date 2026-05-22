def can_place_flowers(flowerbed: list, n: int) -> bool:
    """
    Return True if n flowers can be planted in the flowerbed without
    placing two flowers in adjacent spots.

    The flowerbed is encoded as a list of 0s and 1s:
    - 0 means the spot is empty (a flower may be planted here).
    - 1 means the spot is already planted.

    A spot can be planted only if both neighbors are 0. Out-of-range
    positions (before index 0, after the last index) are treated as
    empty, so boundary spots only need their one real neighbor to be 0.

    Time: O(m), where m is the length of the flowerbed (single pass).
    Space: O(1), only a counter is used; the flowerbed is updated in place.
    """
    # goal of zero (or fewer) flowers is already satisfied — nothing to do
    if n <= 0:
        return True

    if not all(spot in (0, 1) for spot in flowerbed):
        raise ValueError("flowerbed must contain only 0 and 1")

    def is_empty(idx: int) -> bool:
        if idx < 0 or idx >= len(flowerbed):
            return True
        return flowerbed[idx] == 0

    planted_count: int = 0

    for spot in range(len(flowerbed)):
        if flowerbed[spot] == 1:
            continue

        if is_empty(spot - 1) and is_empty(spot + 1):
            # plant here, then mark the spot so the next iteration
            # sees it as occupied and won't plant adjacent to it.
            flowerbed[spot] = 1
            planted_count += 1

            if planted_count >= n:
                return True

    return False


if __name__ == "__main__":
    print(can_place_flowers([1, "SA", 0, 0, 1], 1))
    print(can_place_flowers([1, 0, 0, 0, 1], 2))
    print(can_place_flowers([1, 0, 0, 0, 0], 2))
