"""
Performance benchmark for first_unique_char implementations.

Constraints honored:
    1 <= len(s) <= 100_000
    s consists of lowercase English letters only (a-z)
    s is non-empty
"""

import random
import string
import timeit


# ---------------------------------------------------------------------------
# Implementations under test
# ---------------------------------------------------------------------------
def first_unique_char(s: str) -> int:
    s_dict: dict[str, int] = {}
    s_pos_dict: dict[str, int] = {}

    for i, char in enumerate(s):
        s_dict[char] = s_dict.get(char, 0) + 1
        if s_pos_dict.get(char, 0) == 0:
            s_pos_dict[char] = i

    for char in s_dict:
        if s_dict[char] == 1:
            return s_pos_dict[char]

    return -1


def first_unique_char_claude(s: str) -> int:
    counts: dict[str, int] = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1

    for i, char in enumerate(s):
        if counts[char] == 1:
            return i

    return -1


# ---------------------------------------------------------------------------
# Test-case generators (each returns a string within the constraints)
# ---------------------------------------------------------------------------
def make_unique_at_start(n: int) -> str:
    # 'a' is unique and sits at index 0; the rest are 'b'
    return "a" + "b" * (n - 1)


def make_unique_at_end(n: int) -> str:
    # forces a full scan: 'z' is the only unique char, at the very end
    return "a" * (n - 1) + "z"


def make_no_unique(n: int) -> str:
    # every char appears exactly twice -> returns -1 (worst case, full scan)
    half = "".join(random.choice(string.ascii_lowercase) for _ in range(n // 2))
    return half + half


def make_random(n: int) -> str:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(n))


SCENARIOS = {
    "unique_at_start (best case)": make_unique_at_start,
    "unique_at_end (full scan)": make_unique_at_end,
    "no_unique / returns -1": make_no_unique,
    "random": make_random,
}

IMPLEMENTATIONS = {
    "first_unique_char (2 dicts)": first_unique_char,
    "first_unique_char_claude (1 dict)": first_unique_char_claude,
}

SIZES = [1_000, 10_000, 100_000]
REPEATS = 5          # timeit.repeat rounds; we take the min (least noisy)
NUMBER = 50          # executions per round


# ---------------------------------------------------------------------------
# Correctness check before timing (a fast function that returns wrong answers
# is not a useful benchmark)
# ---------------------------------------------------------------------------
def verify_agreement() -> None:
    print("Verifying both functions agree on outputs...")
    random.seed(42)
    for name, gen in SCENARIOS.items():
        for n in (1, 2, 10, 1_000):
            s = gen(max(n, 2))
            a = first_unique_char(s)
            b = first_unique_char_claude(s)
            status = "OK" if a == b else f"MISMATCH a={a} b={b}"
            if a != b:
                print(f"  [{name}] n={n}: {status}  sample={s[:20]!r}")
    print("  done.\n")


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def run() -> None:
    verify_agreement()

    header = f"{'scenario':<28}{'n':>8}{'impl':<36}{'best ms':>12}"
    print(header)
    print("-" * len(header))

    random.seed(42)
    for scenario_name, gen in SCENARIOS.items():
        for n in SIZES:
            s = gen(n)  # build ONCE so both impls time the same input
            for impl_name, fn in IMPLEMENTATIONS.items():
                # time only the function call, not string construction
                best = min(
                    timeit.repeat(lambda: fn(s), repeat=REPEATS, number=NUMBER)
                )
                per_call_ms = (best / NUMBER) * 1_000
                print(
                    f"{scenario_name:<28}{n:>8}{impl_name:<36}{per_call_ms:>12.4f}"
                )
            print()


if __name__ == "__main__":
    run()
