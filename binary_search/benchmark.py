"""Performance benchmark for binary-search implementations (LeetCode 704).

Constraints: 0 <= len(nums) <= 10^5; -10^9 <= nums[i] <= 10^9; nums sorted
ascending, no duplicates; target in the same range.

n = length of the input list.

The dominant variable for search is *where the target sits*: linear scan cost
is proportional to the target's index, while binary search and bisect are
O(log n) regardless of position. The workloads below vary the target position
(and include the not-present case) to expose that.
"""

import bisect
import random
import timeit
from statistics import median


# ---------------------------------------------------------------------------
# Implementations
# ---------------------------------------------------------------------------


def search_linear(nums: list[int], target) -> int:
    # Time O(n), Space O(1)
    for i, num in enumerate(nums):
        if target == num:
            return i
    return -1


def search_binary(nums: list[int], target) -> int:
    # Time O(log n), Space O(1)
    left = 0
    right = len(nums) - 1
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
    # Time O(log n) (C-level), Space O(1)
    # NOTE: import moved to module top; importing inside the function adds a
    # dict lookup per call (cached, but still measurable in a hot loop).
    index = bisect.bisect_left(nums, target)
    if index < len(nums) and nums[index] == target:
        return index
    return -1


IMPLS = {
    "linear": search_linear,
    "binary": search_binary,
    "bisect": search_built_in,
}


# ---------------------------------------------------------------------------
# Data + target builders
#
# Each builder returns (nums, target). nums is a sorted, duplicate-free list of
# length ~n drawn from the allowed value range; target is chosen to land at a
# particular position (or to be absent).
# ---------------------------------------------------------------------------

LO, HI = -(10**9), 10**9


def _sorted_unique(n: int) -> list[int]:
    """n distinct sorted ints within the allowed range."""
    n = max(1, n)
    return sorted(random.sample(range(LO, HI), n))


def target_at_front(n):
    nums = _sorted_unique(n)
    return nums, nums[0]


def target_at_middle(n):
    nums = _sorted_unique(n)
    return nums, nums[len(nums) // 2]


def target_at_end(n):
    nums = _sorted_unique(n)
    return nums, nums[-1]


def target_random(n):
    nums = _sorted_unique(n)
    return nums, random.choice(nums)


def target_absent(n):
    """Target guaranteed not in nums (linear's true worst case: full scan)."""
    nums = _sorted_unique(n)
    t = nums[-1] + 1 if nums[-1] < HI - 1 else nums[0] - 1
    return nums, t


WORKLOADS = {
    "target_at_front": target_at_front,
    "target_at_middle": target_at_middle,
    "target_at_end": target_at_end,
    "target_random": target_random,
    "target_absent": target_absent,
}


# ---------------------------------------------------------------------------
# Correctness cross-check (linear is the reference)
# ---------------------------------------------------------------------------


def verify():
    extra = [
        ([], 5),
        ([1], 1),
        ([1], 2),
        ([-3, 0, 4, 9], -3),
        ([-3, 0, 4, 9], 9),
        ([-3, 0, 4, 9], 5),
    ]
    cases = [maker(999) for maker in WORKLOADS.values()] + extra
    for nums, target in cases:
        ref = search_linear(nums, target)
        for name, fn in IMPLS.items():
            got = fn(nums, target)
            # linear returns first match; with no duplicates all must agree.
            if got != ref:
                raise AssertionError(
                    f"{name} disagreed (got {got}, expected {ref}) "
                    f"on len {len(nums)}, target {target}"
                )
    print("Correctness: all three agree on every check case.\n")


# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------


def bench(n, repeats, number):
    print(
        f"{'=' * 70}\nn = {n:,} elements   "
        f"(repeats={repeats}, number={number}, median per call)\n{'=' * 70}"
    )
    header = f"{'workload':<20}" + "".join(f"{name:>14}" for name in IMPLS)
    print(header)
    print("-" * len(header))
    for label, maker in WORKLOADS.items():
        nums, target = maker(n)
        row = f"{label:<20}"
        for name, fn in IMPLS.items():
            samples = timeit.repeat(
                lambda: fn(nums, target), repeat=repeats, number=number
            )
            per_call_us = (median(samples) / number) * 1e6
            row += f"{per_call_us:>12.2f}\u00b5s"
        print(row)
    print()


if __name__ == "__main__":
    random.seed(42)
    verify()
    bench(n=100, repeats=200, number=100)
    bench(n=1_000, repeats=200, number=50)
    bench(n=10_000, repeats=100, number=20)
    bench(n=100_000, repeats=50, number=10)  # max constraint
