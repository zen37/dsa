"""Performance benchmark for single_number implementations (LeetCode 136).

Constraints: 1 <= len(nums) <= 30_000; every element appears twice except one;
integers may be negative, zero, or large.

n = length of the input list.
"""

import functools
import operator
import random
import timeit
from statistics import median


# ---------------------------------------------------------------------------
# Implementations
# ---------------------------------------------------------------------------


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


def single_number_xor(nums: list[int]) -> int:
    # Time: O(n), Space: O(1) -- canonical answer
    # a ^ a == 0 and x ^ 0 == x, so all paired elements cancel,
    # leaving only the unique one.
    result = 0
    for num in nums:
        result ^= num
    return result


def single_number_xor_reduce(nums: list[int]) -> int:
    # Same idea, expressed as a single C-level reduce over operator.xor.
    return functools.reduce(operator.xor, nums)


IMPLS = {
    "dict": single_number_dict,
    "set": single_number_set,
    "xor_loop": single_number_xor,
    "xor_reduce": single_number_xor_reduce,
}


# ---------------------------------------------------------------------------
# Workloads (n = list length; n is forced odd so exactly one element is unique)
# ---------------------------------------------------------------------------


def _odd(n: int) -> int:
    """Round n up to the nearest odd number >= 1 (need an odd count)."""
    n = max(1, n)
    return n if n % 2 else n + 1


def _build(pairs: list[int], unique: int) -> list[int]:
    """Each value in `pairs` appears twice, plus `unique` once; then shuffle."""
    out = []
    for v in pairs:
        out.append(v)
        out.append(v)
    out.append(unique)
    random.shuffle(out)
    return out


def make_unique_random(n):
    """Unique element sits at a random position (typical case)."""
    n = _odd(n)
    k = (n - 1) // 2
    vals = random.sample(range(-(10**6), 10**6), k + 1)
    return _build(vals[:k], vals[k])


def make_unique_first(n):
    """Unique element placed at index 0 (no shuffle) -- favors dict's early
    return if it happens to scan it first; set/xor are position-agnostic."""
    n = _odd(n)
    k = (n - 1) // 2
    vals = random.sample(range(-(10**6), 10**6), k + 1)
    out = [vals[k]]
    for v in vals[:k]:
        out.append(v)
        out.append(v)
    return out


def make_unique_last(n):
    """Unique element placed at the very end (no shuffle)."""
    n = _odd(n)
    k = (n - 1) // 2
    vals = random.sample(range(-(10**6), 10**6), k + 1)
    out = []
    for v in vals[:k]:
        out.append(v)
        out.append(v)
    out.append(vals[k])
    return out


def make_small_range(n):
    """Values drawn from a tiny range -> many hash collisions / dense ints."""
    n = _odd(n)
    k = (n - 1) // 2
    # values in a small window; still must be distinct pairs, so use 0..k
    vals = list(range(k + 1))
    return _build(vals[:k], vals[k])


WORKLOADS = {
    "unique_random_pos": make_unique_random,
    "unique_first": make_unique_first,
    "unique_last": make_unique_last,
    "small_value_range": make_small_range,
}


# ---------------------------------------------------------------------------
# Correctness cross-check
# ---------------------------------------------------------------------------


def verify():
    cases = [
        [1],
        [2, 2, 1],
        [4, 1, 2, 1, 2],
        [-3, -3, 7],
        [0, 0, -5],
        [10**9, 10**9, -(10**9)],
    ]
    cases += [maker(999) for maker in WORKLOADS.values()]
    for case in cases:
        results = {name: f(list(case)) for name, f in IMPLS.items()}
        ref = results["xor_loop"]
        if any(r != ref for r in results.values()):
            raise AssertionError(f"DISAGREEMENT on len {len(case)}: {results}")
    print("Correctness: all four agree on every check case.\n")


# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------


def bench(n, repeats, number):
    print(
        f"{'=' * 78}\nn = {n:,} elements   "
        f"(repeats={repeats}, number={number}, median per call)\n{'=' * 78}"
    )
    header = f"{'workload':<22}" + "".join(f"{name:>14}" for name in IMPLS)
    print(header)
    print("-" * len(header))
    for label, maker in WORKLOADS.items():
        data = maker(n)
        row = f"{label:<22}"
        for name, fn in IMPLS.items():
            samples = timeit.repeat(lambda: fn(data), repeat=repeats, number=number)
            per_call_us = (median(samples) / number) * 1e6
            row += f"{per_call_us:>12.1f}\u00b5s"
        print(row)
    print()


if __name__ == "__main__":
    random.seed(42)
    verify()
    bench(n=100, repeats=200, number=50)
    bench(n=1_000, repeats=100, number=20)
    bench(n=10_000, repeats=50, number=5)
    bench(n=30_000, repeats=30, number=3)  # max constraint
