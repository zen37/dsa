import timeit
import random
import string

from main import word_count_v1, word_count_v2


def generate_word_list(n: int, unique_words: int) -> list[str]:
    """Generate a list of n words drawn from a vocabulary of unique_words."""
    vocabulary = ["".join(random.choices(string.ascii_lowercase, k=6)) for _ in range(unique_words)]
    return random.choices(vocabulary, k=n)


def benchmark(label: str, func, lst: list[str], iterations: int = 1000) -> float:
    timer = timeit.Timer(lambda: func(lst))
    total = timer.timeit(number=iterations)
    avg_ms = (total / iterations) * 1000
    print(f"{label:<20} {avg_ms:.4f} ms")
    return avg_ms


if __name__ == "__main__":
    ITERATIONS = 1000

    scenarios = [
        ("Small (50u)",     1_000,       50),
        ("Small (200u)",    1_000,      200),
        ("Small (500u)",    1_000,      500),
        ("Small (900u)",    1_000,      900),
        ("Medium (500u)",   100_000,    500),
        ("Medium (5000u)",  100_000,  5_000),
        ("Medium (20000u)", 100_000, 20_000),
        ("Large (500u)",    1_000_000,    500),
        ("Large (5000u)",   1_000_000,  5_000),
        ("Large (20000u)",  1_000_000, 20_000),
    ]

    for name, n, unique in scenarios:
        lst = generate_word_list(n, unique)
        print(f"\n--- {name}: {n:,} words, {unique} unique ---")
        t1 = benchmark("v1 (loop)", word_count_v1, lst, ITERATIONS)
        t2 = benchmark("v2 (Counter)", word_count_v2, lst, ITERATIONS)
        faster = "v2 (Counter)" if t2 < t1 else "v1 (loop)"
        speedup = max(t1, t2) / min(t1, t2)
        print(f"Winner: {faster} by {speedup:.2f}x")
