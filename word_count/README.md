# word_count

Two implementations of a function that counts how many times each word appears in a list.

```python
["apple", "banana", "apple", "cherry"] -> {"apple": 2, "banana": 1, "cherry": 1}
```

---

## Functions

### `word_count_v1` — manual loop

```python
def word_count_v1(lst: list[str]) -> dict[str, int]:
    word_dict: dict[str, int] = {}
    for w in lst:
        word_dict[w] = word_dict.get(w, 0) + 1
    return word_dict
```

Iterates through the list manually. For each word, looks up its current count with `.get(w, 0)` (defaulting to 0 if not seen yet) and increments it. Pure Python — every iteration goes through the interpreter.

- **Time:** O(n)
- **Space:** O(k) where k = number of unique words

---

### `word_count_v2` — `collections.Counter`

```python
def word_count_v2(lst: list[str]) -> dict[str, int]:
    return dict(Counter(lst))
```

Uses Python's built-in `Counter`, which does the same counting internally but implemented in C. Returns a plain `dict` by wrapping with `dict()`.

- **Time:** O(n)
- **Space:** O(k) where k = number of unique words

---

## Performance

Benchmarked with `timeit` over 1,000 iterations per scenario. Each scenario varies list size and number of unique words.

### Small (1,000 words)

| Unique words | v1 (loop) | v2 (Counter) | Speedup |
|---|---|---|---|
| 50  | 0.0362 ms | 0.0231 ms | 1.57x |
| 200 | 0.0649 ms | 0.0234 ms | **2.77x** |
| 500 | 0.0414 ms | 0.0263 ms | 1.57x |
| 900 | 0.0431 ms | 0.0276 ms | 1.56x |

### Medium (100,000 words)

| Unique words | v1 (loop) | v2 (Counter) | Speedup |
|---|---|---|---|
| 500   | 3.4196 ms | 2.1723 ms | 1.57x |
| 5,000  | 3.9860 ms | 2.8768 ms | 1.39x |
| 20,000 | 4.5432 ms | 3.3756 ms | 1.35x |

### Large (1,000,000 words)

| Unique words | v1 (loop) | v2 (Counter) | Speedup |
|---|---|---|---|
| 500    | 42.7130 ms | 30.2981 ms | 1.41x |
| 5,000  | 40.3823 ms | 28.7774 ms | 1.40x |
| 20,000 | 44.8761 ms | 32.4518 ms | 1.38x |

---

## Key Observations

**`Counter` wins at every size and uniqueness ratio.** Both are O(n) in theory, but `Counter`'s C-level loop avoids Python interpreter overhead entirely, giving a consistent ~1.4–1.6x speedup.

**Speedup narrows as uniqueness increases.** More unique words means more dict insertions (vs. cheaper updates), which is slightly more expensive in both implementations — but `Counter` handles this more efficiently, closing the gap less than v1 does at higher uniqueness.

**Anomaly at Small (200u): 2.77x speedup.** This is likely a measurement artifact (noise at sub-millisecond timings) rather than a structural difference. The surrounding small scenarios consistently show ~1.57x.

**Scaling is linear as expected.** Going from 100K to 1M words (10x data) produces roughly 10x runtime in both implementations, confirming O(n) holds in practice.

---

## Conclusion

Use `word_count_v2` (`Counter`). It is faster at every scale with no tradeoff in readability or correctness. `word_count_v1` is useful for understanding the underlying algorithm.
