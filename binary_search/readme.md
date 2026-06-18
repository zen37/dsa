# Binary Search — Implementations & Benchmark

Three approaches to LeetCode 704 (*Binary Search*), compared on correctness and
performance.

**Problem:** given a list `nums` sorted ascending with no duplicates and a
`target`, return the index of `target`, or `-1` if absent.

**Constraints:** `0 <= len(nums) <= 10^5`, `-10^9 <= nums[i] <= 10^9`, sorted
ascending, no duplicates, input always valid.

Throughout: **n = length of the input list**.

> The dominant variable for search is **where the target sits**. Linear scan
> cost is proportional to the target's index; binary search and bisect are
> O(log n) regardless of position. The benchmark varies target position (and
> includes the absent case) precisely to expose that.

---

## The three approaches

### 1. `linear` — scan front to back

```python
for i, num in enumerate(nums):
    if target == num:
        return i
return -1
```

- **Time:** O(n) worst case; O(1) if the target is near the front.
- **Space:** O(1).
- Ignores the fact that `nums` is sorted. Cost grows with the target's index:
  near-instant at the front, full-scan at the end or when absent.

### 2. `binary` — hand-written binary search

```python
left, right = 0, len(nums) - 1
while left <= right:
    mid = (left + right) // 2
    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
return -1
```

- **Time:** O(log n). **Space:** O(1).
- Halves the search space each step. At n = 100,000 that is only ~17 iterations
  (log2(100,000) ≈ 16.6), independent of where the target is.
- Runs in interpreted Python, so each of those ~17 steps carries bytecode
  overhead.

### 3. `bisect` — the standard library

```python
import bisect
index = bisect.bisect_left(nums, target)
return index if index < len(nums) and nums[index] == target else -1
```

- **Time:** O(log n), executed in C. **Space:** O(1).
- Same algorithm as `binary`, but the search loop runs inside CPython's C
  implementation, so the per-step overhead is far lower. `bisect_left` finds the
  insertion point; a single follow-up check confirms an exact match.
- **Note:** put `import bisect` at module level, not inside the function. The
  import is cached, but an in-function import adds a dict lookup per call that is
  measurable in a hot loop.

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| `linear` | O(n) | O(1) | Position-dependent; ignores sortedness |
| `binary` | O(log n) | O(1) | Correct log-time, interpreted |
| `bisect` | O(log n) | O(1) | Same algorithm in C; fastest |

---

## Benchmark

`bench_search.py` verifies all three agree on a set of check cases, then times
them with `timeit` (median per call) across five workloads that differ only in
target position:

- **target_at_front** — index 0 (linear's best case).
- **target_at_middle** — middle index.
- **target_at_end** — last index (linear scans the whole list).
- **target_random** — a random present value (typical case).
- **target_absent** — a value not in the list (linear's true worst case: a full
  scan to confirm `-1`).

Run it:

```bash
python3 bench_search.py
```

---

## Results (median µs per call)

> Hardware/run dependent; the ratios between approaches are the point.

**n = 100**

| workload | linear | binary | bisect |
|----------|-------:|-------:|-------:|
| target_at_front  | 0.12 | 0.33 | **0.10** |
| target_at_middle | 0.92 | 0.31 | **0.09** |
| target_at_end    | 1.69 | 0.35 | **0.10** |
| target_random    | 0.60 | 0.22 | **0.09** |
| target_absent    | 1.69 | 0.36 | **0.09** |

**n = 1,000**

| workload | linear | binary | bisect |
|----------|-------:|-------:|-------:|
| target_at_front  | **0.11** | 0.46 | 0.12 |
| target_at_middle | 9.05 | 0.59 | **0.12** |
| target_at_end    | 19.08 | 0.66 | **0.12** |
| target_random    | 2.44 | 0.57 | **0.11** |
| target_absent    | 19.02 | 0.68 | **0.11** |

**n = 10,000**

| workload | linear | binary | bisect |
|----------|-------:|-------:|-------:|
| target_at_front  | **0.11** | 0.71 | 0.13 |
| target_at_middle | 104.99 | 0.83 | **0.14** |
| target_at_end    | 203.64 | 0.90 | **0.14** |
| target_random    | 34.90 | 0.88 | **0.13** |
| target_absent    | 205.37 | 0.93 | **0.13** |

**n = 100,000 (max constraint)**

| workload | linear | binary | bisect |
|----------|-------:|-------:|-------:|
| target_at_front  | **0.11** | 0.89 | 0.15 |
| target_at_middle | 1056.88 | 1.01 | **0.15** |
| target_at_end    | 2061.55 | 1.08 | **0.15** |
| target_random    | 1665.06 | 1.18 | **0.15** |
| target_absent    | 2073.23 | 1.11 | **0.14** |

---

## What the numbers show

**Linear search is entirely position-bound — and it scales linearly with n.**
On `target_at_front` it is ~0.11µs at *every* size (it returns on the first
iteration, so n is irrelevant). But on `target_at_end` and `target_absent` it
grows in lockstep with n: 1.69µs → 19µs → 204µs → 2,062µs across
100 → 1K → 10K → 100K — a clean ~10× per 10×, exactly O(n). At the max
constraint, finding an end/absent element takes over 2 milliseconds.

**Binary and bisect are essentially flat across position and barely grow with
n.** Both stay near 1µs (binary) and 0.15µs (bisect) even at 100,000 elements,
because the work is ~17 halving steps regardless of where the target is or
whether it is present. The tiny growth that does appear (binary: 0.33 → 1.1µs
from n=100 to 100K) is just the extra log-steps — about +4 comparisons across
that range.

**At the max constraint, the gap is enormous.** For an absent target at
n=100,000: `bisect` ~0.14µs vs `linear` ~2,073µs — roughly a **15,000×
difference**. Even hand-written `binary` (~1.1µs) is ~1,900× faster than linear
there. This is the O(log n) vs O(n) divide made concrete.

**`bisect` beats hand-written `binary` by ~7–8×** at every size (e.g. 0.15 vs
1.08µs at 100K). Identical algorithm — the difference is purely that
`bisect_left` runs its loop in C while `binary` pays Python bytecode overhead on
each of the ~17 steps. Same complexity, much smaller constant.

**The one case linear wins:** `target_at_front`. At ~0.11µs it edges out even
`bisect` (~0.15µs), because a single comparison beats setting up a bisect call.
But this is a degenerate best case — it requires the target to be the very first
element, which you cannot rely on.

---

## Recommendation

- **Default / production:** `bisect`. Fastest by a wide margin, O(log n), and
  it is the standard library — no hand-rolled index arithmetic to get wrong.
- **Interview answer:** `binary`. The expected solution for "implement binary
  search" — demonstrates you can manage the `left`/`right`/`mid` invariants and
  the `<=` loop condition. Mention that `bisect` is what you would use in real
  code.
- **`linear`:** only defensible when the list is tiny, unsorted, or the target
  is reliably near the front. On a sorted list it throws away the structure that
  makes O(log n) possible — at 100K elements it is ~2,000× slower for end/absent
  targets.

**Bottom line:** on sorted data, log-time search is not a micro-optimization —
it is the difference between ~0.15µs and ~2ms at the maximum input size. Use
`bisect`; implement `binary` when asked to show the algorithm.