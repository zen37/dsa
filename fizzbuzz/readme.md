Because the original code **recomputes the same modulo operations multiple times per iteration**. The cached version computes each one exactly once.

**Let's trace the original for `i = 7` (divisible by neither):**

```python
if i % 3 == 0 and i % 5 == 0:   # compute i % 3 → False; short-circuit skips i % 5
elif i % 3 == 0:                # RECOMPUTE i % 3 → False  ← duplicate work
elif i % 5 == 0:                # compute i % 5 → False
else:
    result.append(str(i))
```

For `i = 7`, Python computes `i % 3` **twice** — once in the first `if`, once again in the `elif`. That's wasted work.

**Now trace `i = 6` (divisible by 3 only):**

```python
if i % 3 == 0 and i % 5 == 0:   # i % 3 → True, then i % 5 → False
elif i % 3 == 0:                # RECOMPUTE i % 3 → True  ← duplicate work
    result.append("Fizz")
```

Again `i % 3` is computed twice.

**Modulo count per iteration (original):**

| Case | Frequency | Modulos computed |
|---|---|---|
| Divisible by 15 | 1/15 | 2 (`i%3`, `i%5`) |
| Divisible by 3 only | 4/15 | 3 (`i%3`, `i%5`, `i%3` again) |
| Divisible by 5 only | 2/15 | 2 (`i%3`, `i%3` again, `i%5`) wait — actually 3 |
| Neither | 8/15 | 3 (`i%3`, `i%3` again, `i%5`) |

Average: about **2.8 modulos per iteration**.

**Cached version:**

```python
div3 = i % 3 == 0    # compute i % 3 once
div5 = i % 5 == 0    # compute i % 5 once

if div3 and div5:    # just reads two booleans
elif div3:           # reads a boolean
elif div5:           # reads a boolean
```

You compute each modulo **exactly once per iteration**. Flat **2 modulos per iteration**, regardless of which branch wins.

**Net savings: ~28% fewer modulo operations on average.**

**Why this matters (and where it doesn't):**

- Reading a cached boolean (`div3`) is essentially free — just a `LOAD_FAST` bytecode.
- Computing `i % 3` is a real arithmetic operation — fast on modern CPUs, but slower than a variable read.

So caching trades a tiny amount of memory (two booleans) for skipping repeated arithmetic. The Big-O is the same (`O(n)` either way), but the constant factor shrinks.

**Magnitude in practice:**

For `n = 1_000_000`, this might save a few milliseconds. For `n = 100`, it saves microseconds. The performance gain is real but small — the **bigger argument for caching is clarity**: each fact about `i` (divisible by 3? by 5?) is stated once, named, and reused. That's better engineering, independent of the speed win.