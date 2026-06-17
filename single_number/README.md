# Single Number — Implementations & Benchmark

Four approaches to LeetCode 136 (*Single Number*), compared on correctness and
performance.

**Problem:** every element in the list appears exactly twice except for one,
which appears once. Return that single element.

**Constraints:** `1 <= len(nums) <= 30_000`; every element appears twice except
one; integers may be negative, zero, or large.

Throughout: **n = length of the input list**.

---

## The four approaches

### 1. `dict` — count occurrences, then find the count-1 key

```python
nums_dict = {}
for num in nums:
    nums_dict[num] = nums_dict.get(num, 0) + 1
for key in nums_dict:
    if nums_dict[key] == 1:
        return key
```

- **Time:** O(n). **Space:** O(n) — a counter entry per distinct value.
- Two passes: build the counts, then scan the keys for the one with count 1.
  Per element it hashes, calls `.get()`, and stores an integer count. The most
  work of the four for the same asymptotic bound.

### 2. `set` — toggle membership; survivor is the answer

```python
nums_set = set()
for num in nums:
    if num in nums_set:
        nums_set.remove(num)
    else:
        nums_set.add(num)
return nums_set.pop()
```

- **Time:** O(n). **Space:** O(n) worst case, but shrinks as pairs cancel.
- One pass: add a value the first time seen, remove it the second. After the
  pass only the unique element remains. Less per-element work than `dict` (no
  counter, no second pass), so consistently faster than it.

### 3. `xor_loop` — XOR accumulation (canonical)

```python
result = 0
for num in nums:
    result ^= num
return result
```

- **Time:** O(n). **Space:** O(1) — a single accumulator.
- Relies on two XOR identities: `a ^ a == 0` (equal values cancel) and
  `x ^ 0 == x`. XOR-ing the whole list cancels every pair and leaves the unique
  element. The textbook answer: optimal space, one cheap integer op per element,
  no hashing or allocation.

### 4. `xor_reduce` — same idea, folded at C level

```python
return functools.reduce(operator.xor, nums)
```

- **Time:** O(n). **Space:** O(1).
- Identical logic to `xor_loop`, but the fold runs entirely in C via
  `functools.reduce` + `operator.xor`, avoiding per-iteration Python bytecode.
  A pure constant-factor win over the explicit loop.

| Approach | Time | Extra space | Notes |
|----------|------|-------------|-------|
| `dict`       | O(n) | O(n) | Two passes; counter per value; slowest |
| `set`        | O(n) | O(n) | One pass; cancels pairs; faster than dict |
| `xor_loop`   | O(n) | O(1) | Canonical; optimal space |
| `xor_reduce` | O(n) | O(1) | Canonical, folded in C; fastest |

---

## Benchmark

`bench_single_number.py` verifies all four agree on a set of check cases, then
times them with `timeit` (median per call) across four workloads. Every
workload uses an odd-length list (one unique element, the rest in pairs); most
shuffle the unique element's position so no approach can exploit input order.

- **unique_random_pos** — unique element at a random position (typical case).
- **unique_first** — unique element at index 0.
- **unique_last** — unique element at the end.
- **small_value_range** — values drawn from a tiny dense range (stresses
  hashing for the dict/set approaches).

Run it:

```bash
python3 bench_single_number.py
```

---

## Results (median µs per call)

> Hardware/run dependent; the ratios between approaches are the point.

**n = 100**

| workload | dict | set | xor_loop | xor_reduce |
|----------|-----:|----:|---------:|-----------:|
| unique_random_pos | 5.2 | 2.9 | 1.9 | **1.7** |
| unique_first      | 3.7 | 3.2 | 1.9 | **1.8** |
| unique_last       | 4.6 | 2.9 | 1.6 | **1.4** |
| small_value_range | 4.0 | 2.9 | 1.3 | **1.0** |

**n = 1,000**

| workload | dict | set | xor_loop | xor_reduce |
|----------|-----:|----:|---------:|-----------:|
| unique_random_pos | 47.7 | 31.6 | 17.7 | **16.6** |
| unique_first      | 37.5 | 27.7 | 18.2 | **16.6** |
| unique_last       | 47.5 | 28.2 | 15.1 | **13.0** |
| small_value_range | 42.7 | 30.4 | 18.5 | **16.8** |

**n = 10,000**

| workload | dict | set | xor_loop | xor_reduce |
|----------|-----:|----:|---------:|-----------:|
| unique_random_pos | 624.5 | 372.5 | 184.1 | **165.3** |
| unique_first      | 381.4 | 298.8 | 182.1 | **165.6** |
| unique_last       | 511.9 | 299.3 | 153.8 | **130.0** |
| small_value_range | 389.7 | 304.2 | 189.9 | **171.4** |

**n = 30,000 (max constraint)**

| workload | dict | set | xor_loop | xor_reduce |
|----------|-----:|----:|---------:|-----------:|
| unique_random_pos | 1521.8 | 1109.5 | 555.0 | **495.3** |
| unique_first      | 1191.6 | 879.8 | 545.1 | **495.5** |
| unique_last       | 1542.5 | 890.8 | 462.1 | **390.4** |
| small_value_range | 1396.3 | 959.4 | 564.7 | **504.0** |

---

## What the numbers show

**The ordering is consistent everywhere:**
`xor_reduce` < `xor_loop` < `set` < `dict`.

**XOR wins on both axes — speed and space.** At the max constraint (n=30,000,
random position) `xor_reduce` runs in ~495µs vs `dict`'s ~1,522µs — about
**3.1× faster** — while using O(1) space instead of O(n). It does one cheap
integer operation per element and stores only a running accumulator: no hashing,
no allocation, no second pass.

**`xor_reduce` edges out `xor_loop`** by running the whole fold at C level
(`functools.reduce` + `operator.xor`), avoiding per-iteration Python bytecode.
Same O(n) time and O(1) space — a constant-factor improvement of roughly
**10–15%** (e.g. 462 vs 390µs on `unique_last` at 30K).

**`set` beats `dict` by ~1.4–1.7×** because it does less per element (add/remove
vs a `.get()` plus a counter object) and makes a single pass, skipping the
dict's second scan over the keys. The set also shrinks as pairs cancel, keeping
its working set small. At 30K random, `set` ~1,110µs vs `dict` ~1,522µs.

**`dict` is slowest** — two passes plus a `.get()` call and an integer-count
object per element. Most work for the same asymptotic bound.

**Scaling is clean and linear** for all four: each ~10× increase in n multiplies
the time by ~10× (e.g. `xor_reduce` random: 16.6 → 165.3 → ~495µs across
1K → 10K → 30K). No approach degrades super-linearly; the differences are
entirely constant-factor.

**The `unique_first` column is a build artifact, not an early exit.** `dict`
looks faster there (1,191µs vs 1,522µs random at 30K), but that reflects how
that workload is constructed (no shuffle), not an algorithmic shortcut — none of
these approaches can terminate early on position, since all must consume the
whole list to confirm the rest pairs up. XOR is essentially flat across layouts,
as expected for a position-agnostic fold.

---

## Recommendation

- **Default / interview answer:** XOR. It is the canonical solution precisely
  because it is the only O(1)-space approach — and it is also the fastest.
  Explain it as "equal values cancel under XOR (`a ^ a == 0`), leaving the
  unique element," and note it needs no extra storage.
  - Write `xor_loop` for clarity, or `xor_reduce` if you want the tightest
    constant factor and like the one-liner.
- **`set`:** a reasonable hash-based answer if you want to show the
  cancellation idea without bit tricks — ~1.4–1.7× faster than `dict`, still
  O(n) space.
- **`dict`:** correct and demonstrates counting, but does the most work and uses
  O(n) space; the one to improve upon if asked.

**Bottom line:** XOR is both the space-optimal and the fastest solution (~3×
ahead of `dict` at the max size). The hash-based approaches are correct and
intuitive but strictly heavier; reach for `set` over `dict` if you avoid the
bitwise trick.