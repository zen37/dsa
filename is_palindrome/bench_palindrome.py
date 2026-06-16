"""Performance benchmark for is_palindrome implementations.

Constraints: 0 <= len(s) <= 200_000, printable ASCII only.

n = length of the input string.
"""

import random
import string
import timeit
from statistics import median


# ---------------------------------------------------------------------------
# Implementations
# ---------------------------------------------------------------------------

_ALNUM = set(string.ascii_lowercase + string.digits)


def pal_set_twoptr(s: str) -> bool:
    # Time: O(n); Space: O(1) - no filtered copy

    if s == "":
        return True

    left: int = 0
    right: int = len(s) - 1

    alphanumeric_set = {
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    }

    while left < right:
        if s[left] not in alphanumeric_set:
            left += 1
        elif s[right] not in alphanumeric_set:
            right -= 1
        elif s[left].lower() != s[right].lower():
            return False
        else:
            left += 1
            right -= 1

    return True


def pal_isalnum_twoptr(s: str) -> bool:
    """Two-pointer, str.isalnum() instead of a set. O(1) space."""
    left, right = 0, len(s) - 1
    while left < right:
        if not s[left].isalnum():
            left += 1
        elif not s[right].isalnum():
            right -= 1
        elif s[left].lower() != s[right].lower():
            return False
        else:
            left += 1
            right -= 1
    return True


def pal_slice(s: str) -> bool:
    """Filter to a list, compare against its reverse. O(n) space."""
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]


def pal_concat(s: str) -> bool:
    """Build filtered string via repeated concatenation, then reverse-compare."""
    if s == "":
        return True
    s = s.lower()
    s_new = ""
    for char in s:
        if char in _ALNUM:
            s_new = s_new + char
    return s_new == s_new[::-1]


IMPLS = {
    "set_2ptr": pal_set_twoptr,
    "isalnum_2ptr": pal_isalnum_twoptr,
    "slice": pal_slice,
    "concat": pal_concat,
}


# ---------------------------------------------------------------------------
# Workloads (n = string length)
# ---------------------------------------------------------------------------


def make_valid_palindrome(n):
    """A true palindrome of length n (worst case: must scan everything)."""
    half = "".join(random.choices(string.ascii_lowercase, k=n // 2))
    mid = random.choice(string.ascii_lowercase) if n % 2 else ""
    return half + mid + half[::-1]


def make_mismatch_at_0(n):
    """Differs at the very ends -> earliest exit for two-pointer."""
    body = "a" * (n - 1)
    return "b" + body  # first char 'b', last char 'a' -> immediate mismatch


def make_mismatch_at_mid(n):
    """Palindrome except the two middle chars -> latest possible exit."""
    s = list(make_valid_palindrome(n))
    if n >= 2:
        mid = n // 2
        # flip one middle char so the mismatch is found only near the center
        s[mid] = "z" if s[mid] != "z" else "y"
    return "".join(s)


def make_heavy_punct(n):
    """Mostly non-alphanumeric chars around a small real palindrome."""
    punct = "".join(random.choices(" .,!?;:-_", k=max(0, n - 4)))
    return "a" + punct[: n // 2] + "bb" + punct[n // 2 :] + "a"


WORKLOADS = {
    "valid_palindrome": make_valid_palindrome,
    "mismatch_at_0": make_mismatch_at_0,
    "mismatch_at_mid": make_mismatch_at_mid,
    "heavy_punct": make_heavy_punct,
}


# ---------------------------------------------------------------------------
# Correctness cross-check
# ---------------------------------------------------------------------------


def verify():
    cases = [
        "",
        "a",
        "A man, a plan, a canal: Panama",
        "race a car",
        "0P",
        " ",
        ".,",
        "ab_a",
        "Was it a car or a cat I saw?",
    ]
    cases += [maker(1000) for maker in WORKLOADS.values()]
    for case in cases:
        results = {name: f(case) for name, f in IMPLS.items()}
        ref = results["isalnum_2ptr"]
        if any(r != ref for r in results.values()):
            raise AssertionError(f"DISAGREEMENT on {case[:30]!r}: {results}")
    print("Correctness: all four agree on every check case.\n")


# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------


def bench(n, repeats, number):
    print(
        f"{'=' * 78}\nn = {n:,} chars   "
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
    bench(n=1_000, repeats=50, number=5)
    bench(n=10_000, repeats=30, number=3)
    bench(n=50_000, repeats=10, number=1)
    bench(n=200_000, repeats=5, number=1)
