# Valid Palindrome — Implementations & Benchmark

Four approaches to LeetCode 125 (*Valid Palindrome*), compared on correctness
and performance.

**Problem:** return `True` if a string reads the same forward and backward
after keeping only alphanumeric characters and lowercasing. Return `False`
otherwise.

**Constraints:** `0 <= len(s) <= 200_000`, printable ASCII only.

Throughout: **n = length of the input string**.

---

## The four approaches

### 1. `set_2ptr` — two-pointer + set membership

Two pointers walk inward from both ends. Each raw character is tested for
membership in a 62-entry alphanumeric set (`a-z`, `A-Z`, `0-9`); non-members
are skipped. Only when *both* pointers sit on alphanumeric chars are those two
lowercased and compared.

```python
if s[left] not in alphanumeric_set:        # raw membership, no .lower()
    left += 1
elif s[right] not in alphanumeric_set:
    right -= 1
elif s[left].lower() != s[right].lower():  # .lower() only on the compared pair
    return False
```

- **Time:** O(n), with **early exit** on the first mismatch.
- **Space:** O(1) extra (the set is a fixed 62 entries, independent of n).
- Because the set includes both cases, the membership test runs on the raw
  char — no per-char `.lower()`. `.lower()` is paid only on matched alphanumeric
  pairs, not on skipped punctuation. This makes it competitive with — and on
  several workloads faster than — `isalnum_2ptr`.

### 2. `isalnum_2ptr` — two-pointer + `str.isalnum()`

Identical structure, but uses the built-in `str.isalnum()` for the filter check
instead of a set lookup.

- **Time:** O(n), with **early exit**.
- **Space:** O(1) extra.
- One C-level method call per filter check, and no hand-maintained set. Trades
  places with `set_2ptr` depending on workload; the cleaner of the two.

### 3. `slice` — filter to a list, reverse-compare

```python
cleaned = [c.lower() for c in s if c.isalnum()]
return cleaned == cleaned[::-1]
```

- **Time:** O(n), but **no early exit** — always builds the full filtered list.
- **Space:** O(n) for the filtered list (plus its reverse).
- Heavy lifting happens at C level (comprehension, slice, `==`), so it beats
  the Python-level two-pointer loops on full scans.

### 4. `concat` — build filtered string by repeated concatenation

```python
s_new = ""
for char in s:
    if char in alnum:
        s_new = s_new + char
return s_new == s_new[::-1]
```

- **Time:** O(n²) *in principle* — `s_new = s_new + char` rebuilds the string
  each iteration. **But CPython** has an in-place optimization that fires when
  `s_new` has a single reference, collapsing it to amortized O(n) here.
- **Space:** O(n) for the built string; **no early exit**.
- The benchmark confirms linear scaling. But the optimization is **fragile**:
  on PyPy, or if the partial string is referenced elsewhere, this reverts to
  quadratic. Prefer `"".join(...)` in real code; keep the O(n²) label as the
  safe description.

| Approach | Time | Extra space | Early exit | Notes |
|----------|------|-------------|------------|-------|
| `set_2ptr`     | O(n) | O(1) | Yes | 62-entry set; `.lower()` only on matches |
| `isalnum_2ptr` | O(n) | O(1) | Yes | Built-in; no set to maintain |
| `slice`        | O(n) | O(n) | No  | Fast full scan via C ops |
| `concat`       | O(n²)\* | O(n) | No | \*amortized O(n) on CPython only |

---

## Benchmark

`bench_palindrome.py` verifies all four agree on a set of check cases, then
times them with `timeit` (median per call) across four workloads:

- **valid_palindrome** — a true palindrome; forces a full scan (worst case).
- **mismatch_at_0** — differs at the very ends; earliest possible exit.
- **mismatch_at_mid** — palindrome except the middle; latest possible exit.
- **heavy_punct** — mostly non-alphanumeric chars; lots of skipping.

Run it:

```bash
python3 bench_palindrome.py
```

---

## Results (median µs per call)

> Hardware/run dependent; the ratios between approaches are the point.

**n = 1,000**

| workload | set_2ptr | isalnum_2ptr | slice | concat |
|----------|---------:|-------------:|------:|-------:|
| valid_palindrome | 63.1 | 54.9 | 37.8 | **35.7** |
| mismatch_at_0    | 0.4 | **0.2** | 29.0 | 33.7 |
| mismatch_at_mid  | 57.9 | 63.7 | **30.8** | 34.0 |
| heavy_punct      | 47.6 | 38.3 | **10.4** | 15.1 |

**n = 10,000**

| workload | set_2ptr | isalnum_2ptr | slice | concat |
|----------|---------:|-------------:|------:|-------:|
| valid_palindrome | 572.9 | 539.1 | **355.5** | 387.6 |
| mismatch_at_0    | 0.4 | **0.2** | 277.1 | 378.6 |
| mismatch_at_mid  | 574.1 | 521.1 | **321.1** | 384.7 |
| heavy_punct      | 490.6 | 407.3 | **103.1** | 158.7 |

**n = 50,000**

| workload | set_2ptr | isalnum_2ptr | slice | concat |
|----------|---------:|-------------:|------:|-------:|
| valid_palindrome | 2919.3 | 2663.8 | **1924.9** | 2044.1 |
| mismatch_at_0    | 0.6 | **0.3** | 1504.8 | 1973.8 |
| mismatch_at_mid  | 2895.8 | 2605.9 | **1693.3** | 1984.4 |
| heavy_punct      | 2617.3 | 2023.9 | **536.2** | 799.6 |

**n = 200,000 (max constraint)**

| workload | set_2ptr | isalnum_2ptr | slice | concat |
|----------|---------:|-------------:|------:|-------:|
| valid_palindrome | 11681.3 | 10600.2 | **8186.8** | 8226.7 |
| mismatch_at_0    | 0.6 | **0.3** | 6464.2 | 8167.5 |
| mismatch_at_mid  | 11635.5 | 10520.0 | **7200.8** | 8302.3 |
| heavy_punct      | 10239.2 | 8140.3 | **2086.3** | 3166.3 |

---

## What the numbers show

**Early exit is the single biggest factor — and only the two-pointer versions
have it.** On `mismatch_at_0`, both `*_2ptr` versions return in **~0.2–0.6µs
regardless of n** (still sub-microsecond at 200,000 chars) by comparing the two
ends and bailing immediately. `slice` and `concat` must build the entire
filtered sequence first, so they pay full price (~6,500–8,200µs at 200K) even
when the answer is decided by the first character — a **~25,000× difference**
on identical input.

**On full scans, the C-level filters win.** When no early exit is possible
(`valid_palindrome`, `mismatch_at_mid`), `slice` leads — ~8,200µs vs
`isalnum_2ptr`'s ~10,600µs and `set_2ptr`'s ~11,700µs at 200K. `concat` tracks
`slice` closely (~8,200–8,300µs). The two-pointer loops run interpreted
per-character work (indexing, comparisons), while `slice`/`concat` push the bulk
of the work into C.

**`heavy_punct` magnifies the C-level advantage.** With most characters skipped,
`slice` filters them out in one C-level pass (~2,086µs at 200K) while the
two-pointer versions still advance one Python iteration per skipped char
(~8,140–10,239µs) — roughly **4–5× slower**.

**`set` and `isalnum` are close, trading places by workload.** With the
`.lower()` removed from the membership test (the set covers both cases, so the
raw char is tested directly), `set_2ptr` no longer pays double per character.
`isalnum_2ptr` is generally a bit faster — a single C-level `.isalnum()` call
versus a Python-level set lookup — but `set_2ptr` wins on some cases (e.g.
`mismatch_at_mid` at n=1,000: 57.9 vs 63.7µs). The differences are small; the
built-in is preferable mainly for needing no hand-maintained set.

**`concat` scales linearly, not quadratically** — confirming CPython's in-place
string optimization fires. It tracks `slice` closely on full scans but is a bit
slower (extra per-char Python loop overhead) and, like `slice`, has no early
exit. Treat its linear behavior as interpreter-specific, not guaranteed.

---

## Recommendation

- **Default / interview answer:** `isalnum_2ptr`. O(1) space, early exit, no
  hand-maintained set. Defend it on worst-case space and best-case early exit.
- **`set_2ptr`:** competitive with `isalnum_2ptr` after dropping the per-char
  `.lower()` — wins on some workloads, loses on others, all by small margins.
  Functionally fine; carries a 62-entry set to maintain.
- **If full scans dominate your inputs (mostly-valid palindromes, heavy
  punctuation):** `slice` is faster in practice on CPython, at O(n) space.
- **`concat`:** avoid as a *pattern* despite its competitive speed. It only
  stays linear thanks to a fragile CPython optimization; use `"".join(...)` if
  you want to build a filtered string.

**Bottom line:** the best choice depends on input distribution. Early mismatches
favor the two-pointer (microseconds vs milliseconds); full scans favor the
C-level filter. The two-pointer is the standard answer for its O(1) space and
early-exit guarantee.
