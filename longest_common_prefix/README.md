# Interpreting the `longest_common_prefix` Benchmarks

This README explains what the numbers in `lcp_benchmarks.md` actually tell you, and which implementation to reach for in which situation. All times are median microseconds (µs) per call; lower is better.

## What was measured

`n` is the number of strings in the list and `m` is the length of each string. Four implementations were timed against four workloads chosen to stress different parts of the algorithm:

- **full_match** — every string shares the entire prefix (`prefix = m`). The worst case for total work: every character must be compared.
- **no_match** — the strings differ at position 0, so the answer is `""`. The best case for an algorithm that can stop early.
- **late_mismatch** — the strings agree until the very last column (`m-1`), then diverge. Almost as much work as full_match.
- **one_short_string** — one string is shorter than the rest, forcing the prefix to end at its length.

The four contenders are `dict`, `vscan` (vertical scan), `zip`, and `column`. The names describe the strategy, not exact code, but the timings make each one's behaviour easy to read off.

## The headline: `dict` does the same work no matter what

The single most important pattern is that `dict` is nearly flat across all four workloads. At n=200, m=200 it costs roughly 7,400µs whether the answer is the full string or the empty string — `no_match` is just as expensive as `full_match`. The other three implementations drop to single-digit microseconds on `no_match` because they stop at the first mismatch; `dict` does not. It pays full price to discover that the answer is `""`.

That gap is enormous at scale. At n=100,000, the `no_match` case costs `dict` about 946,000µs versus 226µs for `column` — over four thousand times slower for the same answer. On top of the missing early-exit, `dict` carries a constant per-character overhead that makes it the slowest contender on every row of every table, typically around 7× slower than `vscan` even on full scans. There is no workload in this data where `dict` is competitive. Treat it as a baseline to beat, not a candidate.

## `zip` wins when you actually have to scan

When the work can't be skipped — `full_match` and `late_mismatch` — `zip` is the clear winner, consistently about 3.8–4× faster than `vscan` or `column`. At n=200, m=200 full_match it's 264µs against roughly 1,070µs for the loop-based approaches. This holds at every scale: at n=100,000 it's ~35ms versus ~130ms for `vscan`.

The reason is that `zip(*strs)` transposes the list into columns at C speed, and comparing a whole column (e.g. with a set) stays in optimized built-in code rather than a Python-level character loop. When most characters have to be examined anyway, that C-level throughput dominates.

## The pure-Python loops win when you can bail early

The picture flips on the early-exit workloads. On `no_match`, `column` is the fastest of all (0.2–0.5µs across sizes), with `vscan` close behind, while `zip` is the slowest of the three fast ones. The same ordering shows up on `one_short_string`.

The reason is fixed overhead. `zip(*strs)` still has to set up the iterator and build the first column tuple before anyone can detect the mismatch, whereas a plain loop can compare `strs[0][0]` against the rest and return immediately. When the answer is decided in column 0, setup cost is the whole cost — and the hand-written loops have less of it.

For tiny inputs the same effect appears even on full scans: at n=2, m=200 full_match, `column` (16.9µs) beats `zip` (22.1µs) because there isn't enough work for `zip`'s transposition to amortize its overhead.

## `column` vs `vscan`

These two are close cousins and usually within a small factor of each other. `column` tends to have slightly lower fixed overhead, so it edges ahead on early exits and on very small `n`. `vscan` is occasionally a hair faster on long full scans (n=200, m=200 full_match: 1,068µs vs 1,124µs). The difference between them is minor compared to the `dict`/`zip`/loop distinctions above, so pick based on readability.

## How it scales

For the full-scan workloads, every implementation grows roughly linearly with the total number of characters compared (`n × m`), which is the expected behaviour — there's no algorithmic blow-up, just different constant factors. The relative gaps stay stable as the input grows: `zip` stays ~4× ahead of the loops, and `dict` stays ~7× behind them on full scans and astronomically behind on early-exit cases. So the choice you make at small scale is the same choice that pays off at large scale.

## Which one to use

| Situation | Best choice | Why |
|---|---|---|
| General default | `zip` | Fastest when characters must be scanned; clean to write |
| Data that usually mismatches early (short/empty common prefix) | `column` or `vscan` | Lowest fixed overhead, exits fastest |
| Very small lists (n ≈ 2) | `column` | `zip` setup cost isn't worth it yet |
| Anything | not `dict` | Strictly dominated on every workload and scale |

In short: if you expect long shared prefixes (sorted strings, file paths, similar identifiers), `zip` is the safe default. If your inputs are heterogeneous and the common prefix is usually short or empty, the early-exit loops are faster and the difference grows with `n`. And `dict`, whatever its appeal as an idea, loses everywhere here because it can't quit early.
