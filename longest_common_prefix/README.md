# Longest Common Prefix — Implementations & Benchmark

Three approaches to LeetCode 14 (*Longest Common Prefix*), compared on
correctness and performance.

**Problem:** given a list of strings, return the longest string that is a
prefix of every element. Return `""` if there is none.

**Constraints:** `0 <= len(strs) <= 200`, `0 <= len(strs[i]) <= 200`,
lowercase English letters only. The benchmark deliberately pushes *past*
these (up to 100 000 strings) to expose scaling behavior.

Throughout: **n = number of strings**, **m = length of a string**.

---

## The three approaches

### 1. `dict` — count (character, position) pairs

Counts every `(char, position)` pair across all strings, then keeps the
leading positions whose count equals `len(strs)`.

```python
def lcp_dict(strs):
    if not strs: return ""
    if len(strs) == 1: return strs[0]
    chars_dict = {}
    for word in strs:
        for i, char in enumerate(word):
            chars_dict[char + str(i)] = chars_dict.get(char + str(i), 0) + 1
    ...
```

- **Time:** O(n·m) — every character of every string is always counted.
- **Space:** O(n·m) — up to one dict entry per distinct `(char, position)`.
- **No early exit:** the full count runs before any answer is computed, so
  cost is identical whether the prefix is empty or full. This is the key
  weakness the benchmark exposes.
- Relies on encoding the position as digits in the key and stripping digits
  at the end — correct only because the inputs are guaranteed digit-free.

### 2. `vscan` — vertical scan (recommended)

Walks character positions of the shortest string; at each position checks
whether all strings agree. First disagreement ends the prefix.

```python
def lcp_vscan(strs):
    if not strs: return ""
    shortest = min(strs, key=len)
    for i, char in enumerate(shortest):
        if any(word[i] != char for word in strs):
            return shortest[:i]
    return shortest
```

- **Time:** O(n·m) worst case; **exits early** the instant a column disagrees.
- **Space:** O(1) extra (output not counted) — streams through a generator,
  never materializing a collection of size n.
- Bounding the scan by the *shortest* string makes in-range indexing obvious.
- Best all-round choice: tightest space, obvious correctness, early exit.

### 3. `zip` — column transpose

`zip(*strs)` yields one column (one char per string) at a time, stopping at
the shortest string automatically.

```python
def lcp_zip(strs):
    prefix = []
    for column in zip(*strs):
        if len(set(column)) == 1:
            prefix.append(column[0])
        else:
            break
    return "".join(prefix)
```

- **Time:** O(n·m); each column builds a set of n chars. Also exits early.
- **Space:** O(n) per-column tuple/set (O(n+m) if the prefix buffer counts).
- Most concise; handles empty and single-element lists for free.
- Faster than `vscan` on long matching prefixes (C-level tuple/set work), but
  always materializes a full column even to reject it, so it loses on the
  trivial early-exit cases.

| Approach | Time | Extra space | Early exit | Notes |
|----------|------|-------------|------------|-------|
| `dict`   | O(n·m) | O(n·m) | No  | Always pays full cost |
| `vscan`  | O(n·m) | O(1)   | Yes | Best balance; recommended |
| `zip`    | O(n·m) | O(n)   | Yes | Most concise; fast on long matches |

---

## Benchmark

`bench_lcp.py` first verifies all three agree on a set of check cases, then
times them with `timeit` (median per call) across four workloads designed to
stress different code paths:

- **full_match** — all strings identical; prefix spans the full length (worst
  case for matching work).
- **no_match** — every string differs at position 0; earliest possible exit.
- **late_mismatch** — common prefix of length m−1, diverging on the last char.
- **one_short_string** — all long and identical except one tiny string, so the
  shortest string caps the scan.

Run it:

```bash
python3 bench_lcp.py
```

---

## Results (median µs per call)

> Hardware/run dependent; absolute numbers will vary, but the *ratios* between
> approaches are the point.

### Within LeetCode constraints (n, m ≤ 200)

**n = 200, m = 200**

| workload | dict | vscan | zip |
|----------|-----:|------:|----:|
| full_match     | 7352.1 | 1074.2 | **264.5** |
| no_match       | 7427.6 | **3.0** | 5.2 |
| late_mismatch  | 7415.7 | 1073.3 | **263.9** |
| one_short      | 7348.5 | 13.6 | **7.2** |

Even the worst case here (`dict`, ~7.4 ms) passes LeetCode comfortably — at
these sizes the choice is about *defending* a solution, not passing.

### Scaling n (m = 50 fixed)

**full_match** (worst case — no early exit helps):

| n | dict | vscan | zip |
|---|-----:|------:|----:|
| 2 000   | 18 733 | 2 617 | **672** |
| 20 000  | 182 023 | 26 287 | **6 820** |
| 100 000 | 944 076 | 132 277 | **34 926** |

**no_match** (early exit dominates):

| n | dict | vscan | zip |
|---|-----:|------:|----:|
| 2 000   | 18 413 | **25.2** | 52.2 |
| 20 000  | 185 008 | **247.6** | 533.3 |
| 100 000 | 921 950 | **1 255.7** | 3 018.6 |

---

## What the numbers show

**`dict` is flat across workloads — and that's its fatal flaw.** At n = 200,
m = 200 it costs ~7.4 ms whether the answer is at position 0 or position 200.
It cannot exit early: the full count always runs first. By n = 100 000 it sits
near **940 ms regardless of input**, while the others finish the trivial cases
in microseconds.

**Early exit is the whole game.** On `no_match` at n = 100 000, `vscan` returns
in ~1.3 ms vs `dict`'s ~922 ms — a **~730× difference on identically sized
input**, purely because `vscan` bails at the first mismatched column.

**`zip` wins long matches; `vscan` wins early exits.** On `full_match`, `zip`
is ~3–4× faster than `vscan` (C-level tuple/set vs Python-level `any`). On
`no_match`/`one_short`, `vscan` edges ahead because `any` short-circuits on the
first differing word without building a full column.

**All scale linearly in n,** as the O(n·m) bound predicts: each ~10× jump in n
multiplies the matching-case times by ~10×.

---

## Recommendation

- **Default / interview answer:** `vscan`. O(1) extra space, obvious
  correctness, clean early-exit story.
- **If you want the most concise code:** `zip`, accepting O(n) per-column
  memory; fastest on long shared prefixes.
- **`dict`:** correct under the constraints but the one to *critique* — heavy
  O(n·m) space and zero early exit make it strictly worse in practice.
