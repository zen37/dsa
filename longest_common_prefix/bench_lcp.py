"""Performance benchmark for three longest_common_prefix implementations.

Constraints honored: 0 <= len(strs) <= 200, 0 <= len(strs[i]) <= 200,
lowercase English letters only.
"""

import random
import string
import timeit
from statistics import median


# ---------------------------------------------------------------------------
# Implementations
# ---------------------------------------------------------------------------


def lcp_dict(strs: list[str]) -> str:
    if not strs:
        return ""
    if len(strs) == 1:
        return strs[0]
    prefix: str = ""
    chars_dict: dict[str, int] = {}
    for word in strs:
        for i, char in enumerate(word):
            chars_dict[char + str(i)] = chars_dict.get(char + str(i), 0) + 1
    first_char_count = next(iter(chars_dict.values()))
    if first_char_count != len(strs):
        return ""
    for key, value in chars_dict.items():
        if value == len(strs):
            prefix += key
        else:
            break
    return "".join([c for c in prefix if not c.isdigit()])


def lcp_vscan(strs: list[str]) -> str:
    if not strs:
        return ""
    shortest = min(strs, key=len)
    for i, char in enumerate(shortest):
        if any(word[i] != char for word in strs):
            return shortest[:i]
    return shortest


def lcp_zip(strs: list[str]) -> str:
    prefix = []
    for column in zip(*strs):
        if len(set(column)) == 1:
            prefix.append(column[0])
        else:
            break
    return "".join(prefix)


def lcp_column(strs: list[str]) -> str:
    if not strs:
        return ""

    first = strs[0]
    for i, char in enumerate(first):  # walk columns of the first string
        for other in strs[1:]:  # check the same column in the rest
            if i >= len(other) or other[i] != char:
                return first[:i]  # mismatch or ran off the end
    return first  # first string is a prefix of all


IMPLS = {"dict": lcp_dict, "vscan": lcp_vscan, "zip": lcp_zip, "column": lcp_column}


# ---------------------------------------------------------------------------
# Workloads (n = number of strings, m = string length)
# ---------------------------------------------------------------------------


def make_full_match(n, m):
    """All strings identical -> prefix spans the full length (worst case)."""
    word = "".join(random.choices(string.ascii_lowercase, k=m))
    return [word] * n


def make_no_match(n, m):
    """Every string differs at position 0 -> earliest possible exit."""
    base = "".join(random.choices(string.ascii_lowercase, k=m - 1))
    return [string.ascii_lowercase[i % 26] + base for i in range(n)]


def make_late_mismatch(n, m):
    """Common prefix of length m-1, diverge on the very last char."""
    base = "".join(random.choices(string.ascii_lowercase, k=m - 1))
    return [base + string.ascii_lowercase[i % 26] for i in range(n)]


def make_one_short(n, m):
    """All long and identical except one tiny string -> shortest caps scan."""
    word = "".join(random.choices(string.ascii_lowercase, k=m))
    out = [word] * (n - 1) + [word[:2]]
    return out


WORKLOADS = {
    "full_match (prefix = m)": make_full_match,
    "no_match (exit at 0)": make_no_match,
    "late_mismatch (exit at m-1)": make_late_mismatch,
    "one_short_string": make_one_short,
}


# ---------------------------------------------------------------------------
# Correctness cross-check before timing
# ---------------------------------------------------------------------------


def verify():
    cases = [
        [],
        ["alone"],
        ["flower", "flow", "flight"],
        ["dog", "racecar", "car"],
        ["", "abc"],
        ["abc", "abc", "abc"],
        ["a"] * 200,
        make_full_match(50, 200),
        make_no_match(50, 200),
        make_late_mismatch(50, 200),
        make_one_short(50, 200),
    ]
    for case in cases:
        results = {name: f(list(case)) for name, f in IMPLS.items()}
        ref = results["vscan"]
        if any(r != ref for r in results.values()):
            raise AssertionError(f"DISAGREEMENT on {case[:3]}...: {results}")
    print("Correctness: all three agree on every check case.\n")


# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------


def bench(n, m, repeats=10, number=5):
    print(
        f"{'=' * 70}\nn = {n} strings, m = {m} chars   "
        f"(repeats={repeats}, number={number}, reporting median per call)\n{'=' * 70}"
    )
    header = f"{'workload':<32}" + "".join(f"{name:>12}" for name in IMPLS)
    print(header)
    print("-" * len(header))
    for label, maker in WORKLOADS.items():
        data = maker(n, m)
        row = f"{label:<32}"
        timings = {}
        for name, fn in IMPLS.items():
            # median of repeats, each timing `number` calls, normalized per call
            samples = timeit.repeat(lambda: fn(data), repeat=repeats, number=number)
            per_call_us = (median(samples) / number) * 1e6
            timings[name] = per_call_us
            row += f"{per_call_us:>10.1f}\u00b5s"
        print(row)
    print()


if __name__ == "__main__":
    random.seed(42)
    verify()
    # Max-constraint corner and a couple of intermediate shapes
    bench(n=200, m=200)
    bench(n=200, m=10)
    bench(n=10, m=200)
    bench(n=2, m=200)
    bench(n=2000, m=50)
    bench(n=20000, m=50)
    bench(n=100000, m=50)
